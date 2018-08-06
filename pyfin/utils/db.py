import psycopg2
import sys
 
def connect_to_database(settings_file_name):
    with open(settings_file_name) as f:
        lines = f.readlines()
    
    #Define our connection string
    conn_string = "host=" + lines[0] + " dbname=" + lines[1] + " user=" + lines[2] + " password=" + lines[3]
 
    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)
 
    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()
    print "Connected!\n"

    return conn, cursor



def insert_names(table, cursor, names):
    count = len(names)

    for i in range (count):
        sql = "INSERT INTO " + table +"(name) SELECT('"+names[i]+"') WHERE NOT EXISTS (SELECT * FROM " + table + " WHERE name='"+names[i]+"');"
        #print sql
        cursor.execute(sql)



def insert_companies(table, cursor, symbols, names, ipo_years, sectors, industries, summary_quotes, stock_exchanges, symbol_suffix):
    count = len(names)

    for i in range (count):
        sql = "INSERT INTO " + table +"(symbol, name, ipo_year, sector_id, industry_id, summary_quote, stock_exchange, symbol_suffix) VALUES('" + symbols[i] + "','" + names[i] + "','" + ipo_years[i] + "', (SELECT sector_id from public.sectors WHERE name='" + sectors[i] + "'), (SELECT industry_id from public.industries WHERE name='" + industries[i] + "'), '" + summary_quotes[i] + "', '" + stock_exchanges[i] + "', '" + symbol_suffix[i] +"');"
        print sql
        cursor.execute(sql)


def get_yahoo_suffix_and_trading_hours_from_symbol(connection, cursor, symbol):
    sql = "SELECT yahoo_suffix, start_time, end_time FROM public.companies INNER JOIN stock_exchanges ON (exchange_id=public.companies.stock_exchange_id) AND (public.companies.symbol='" + symbol + "');"
    cursor.execute(sql)
    rows = cursor.fetchall()
    suffix = ""
    start_time = ""
    end_time = ""

    for row in rows:
        suffix = row[0]
        start_time = row[1]
        end_time = row[2]
    return suffix, start_time, end_time


def get_all_symbols(settings_file_name):
    symbols = []
    conn, cursor = connect_to_database(settings_file_name)
    sql = "SELECT symbol FROM public.companies;"
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        s = row[0]
        suffix, _, _ = get_yahoo_suffix_and_trading_hours_from_symbol(conn, cursor, s)
        symbols.append(s + suffix)

    cursor.close()
    conn.close()
    return symbols


def is_record_in_corrupt_intraday_prices_on_that_day(conn, cur, symbol, date):
    sql = "SELECT * FROM public.corrupt_intraday_prices INNER JOIN public.companies ON (public.corrupt_intraday_prices.company_id=public.companies.company_id) WHERE (public.companies.symbol='" + symbol + "') AND (public.corrupt_intraday_prices.date='" + date + "'::date);"
    cur.execute(sql)
    rows = cur.fetchall()
    if len(rows) == 0:
        return False
    else:
        return True


def add_to_corrupt_intraday_prices(conn, cur, symbol, suffix, date):
    if is_record_in_corrupt_intraday_prices_on_that_day(conn, cur, symbol, date):
        return
    sql = ""
    if suffix =="":
        sql = "INSERT INTO public.corrupt_intraday_prices (company_id, date) VALUES((SELECT company_id FROM public.companies WHERE symbol='" + symbol + "'),'" + date + "'::date);"
    else:
        exchange_id = get_exchange_id_from_suffix(conn, cur, suffix)
        sql = "INSERT INTO public.corrupt_intraday_prices (company_id, date) VALUES((SELECT company_id FROM public.companies WHERE symbol='" + symbol + "' AND stock_exchange_id="+str(exchange_id)+"),'" + date + "'::date);"
    cur.execute(sql)


def get_suffix_list(settings_file_name):
    suffix_list = []
    conn, cursor = connect_to_database(settings_file_name)
    sql = "SELECT yahoo_suffix FROM public.stock_exchanges;"
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        s = row[0]
        if (s != ""):
            suffix_list.append(s)

    cursor.close()
    conn.close()
    return suffix_list


def get_exchange_id_from_suffix(conn, cursor, suffix):
    if suffix == "":
        return None
    sql = "SELECT exchange_id FROM public.stock_exchanges WHERE yahoo_suffix='" + suffix + "';"
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        s = row[0]
        if (s != ""):
            return s

    return None
