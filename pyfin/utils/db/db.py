import sys
sys.path.append("..")

import psycopg2
from utils import time_op, string_op, heal
import os
#from utils.file_system import read
from datetime import datetime, timedelta


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


def get_all_symbols_and_markets(conn, cursor):
    symbols = []
    markets = []
    sql = "SELECT symbol, stock_exchanges.name, stock_exchanges.yahoo_suffix FROM public.companies INNER JOIN public.stock_exchanges ON stock_exchange_id=exchange_id;"
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        s = row[0]
        m = row[1]
        suffix = row[2]
        symbols.append(s + suffix)
        markets.append(m)
    return symbols, markets


def get_company_ids_from_market_and_symbol(conn, cur, market, symbol):
    ids=[]
    exchange_id = get_exchange_id_from_market(conn, cur, market)
    sql = ""
    if exchange_id == None:
        sql ="SELECT company_id FROM public.companies WHERE symbol='" + symbol + "';"
    else:
         sql = "SELECT company_id FROM public.companies WHERE symbol='" + symbol + "' AND stock_exchange_id='"+str(exchange_id)+"';"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        ids.append(row[0])
    return ids


def is_record_in_corrupt_intraday_prices_on_that_day(conn, cur, market, symbol, date):
    company_ids = get_company_ids_from_market_and_symbol(conn, cur, market, symbol)
    if len(company_ids) != 1:
        return True

    sql = "SELECT * FROM public.corrupt_intraday_prices WHERE (company_id='" + str(company_ids[0]) + "') AND (date='" + date + "'::date);"
    cur.execute(sql)
    rows = cur.fetchall()
    if len(rows) == 0:
        return False
    else:
        return True


def is_record_in_intraday_prices_on_that_day_and_time(conn, cur, market, symbol, date, time):
    company_ids = get_company_ids_from_market_and_symbol(conn, cur, market, symbol)
    if len(company_ids) != 1:
        return False

    sql = "SELECT * FROM public.intraday_prices WHERE (company_id='" + str(company_ids[0]) + "') AND (public.intraday_prices.date='" + date + "'::date) AND (public.intraday_prices.time='" + time + "'::time);"
    cur.execute(sql)
    rows = cur.fetchall()
    if len(rows) == 0:
        return False
    else:
        return True




def add_to_corrupt_intraday_prices(conn, cur, market, symbol, date):
    company_ids = get_company_ids_from_market_and_symbol(conn, cur, market, symbol)
    if len(company_ids) != 1:
        return

    sql = "INSERT INTO public.corrupt_intraday_prices (company_id, date) VALUES('" + str(company_ids[0]) + "','" + date + "'::date);"
#    sql = "INSERT INTO public.corrupt_intraday_prices_no_pkey (company_id, date) VALUES('" + str(company_ids[0]) + "','" + date + "'::date);"
    try:
        cur.execute(sql)
    except psycopg2.IntegrityError:
        print "SKIPPING " + sql
        conn.rollback()
    else:
        print sql
        conn.commit()


def process_numeric_value(val):
    processed = '0'
    if val is None:
        processed = 'NaN'
    else:
        processed = str(val)
    return processed


def add_to_intraday_prices(conn, cur, market, symbol, date_time, volume, opn, close, high, low):
    company_ids = get_company_ids_from_market_and_symbol(conn, cur, market, symbol)
    if len(company_ids) != 1:
        return

    count = len(date_time)
    for i in range(count):
        date, time = time_op.get_date_time_from_datetime(date_time[i])
        timestamp = date + " " + time
        vo = process_numeric_value(volume[i])
        op = process_numeric_value(opn[i])
        cl = process_numeric_value(close[i])
        hi = process_numeric_value(high[i])
        lo = process_numeric_value(low[i])
        sql = "INSERT INTO public.intraday_prices (company_id, date_time, volume, opening_price, closing_price, high_price, low_price) VALUES('" + str(company_ids[0]) + "','" + timestamp + "'::timestamp without time zone" + ",'" + vo + "','" + op + "','" + cl + "','" + hi + "','" + lo + "');"
#        sql = "INSERT INTO public.intraday_prices_no_pkey (company_id, date_time, volume, opening_price, closing_price, high_price, low_price) VALUES('" + str(company_ids[0]) + "','" + timestamp + "'::timestamp without time zone" + ",'" + vo + "','" + op + "','" + cl + "','" + hi + "','" + lo + "');"
        try:
            cur.execute(sql)
        except psycopg2.IntegrityError:
            print "SKIPPING " + sql
            conn.rollback()
        else:
            print sql
            conn.commit()


def get_suffix_list(conn, cursor):
    suffix_list = []
    sql = "SELECT yahoo_suffix FROM public.stock_exchanges;"
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        s = row[0]
        if (s != ""):
            suffix_list.append(s)

    return suffix_list


def get_exchange_id_from_market(conn, cursor, market):
    if market == "n_a":
        market = "n/a"
    sql = "SELECT exchange_id FROM public.stock_exchanges WHERE name='" + market + "';"
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        s = row[0]
        if (s != ""):
            return s

    return None

def get_filename_v1_from_item(item):
    filename = os.path.join(item[0], item[1])
    date = time_op.get_date_string_without_padded_zeros(item[2])
    filename = os.path.join(filename, date)
    filename = os.path.join(filename, item[3])
    filename = os.path.join(filename, item[4])
    return filename

'''
def insert_intraday_file_records_v1_into_database(conn, cur, records):
    exchange_dict = {}
    count = len(records)
    for i in range(count):
        item_count = len(records[i])
        for j in range (item_count):
            item = records[i][j]
            filename = get_filename_v1_from_item(item)
            date_time, volume, opn, close, high, low = read.get_all_intraday_data_from_file(filename)
            suffix_list = get_suffix_list(conn, cur)
            symbol_with_suffix = item[1]
            symbol = string_op.get_symbol_without_suffix(symbol_with_suffix, suffix_list)
            market, exchange_dict = get_data_v1_exchange_name_from_symbol(conn, cur, symbol, exchange_dict)
            date = time_op.get_date_string_without_padded_zeros(item[2])
            if read.is_price_list_corrupt(close):
                add_to_corrupt_intraday_prices(conn, cur, market, symbol, date)
            else:
                add_to_intraday_prices(conn, cur, market, symbol, date_time, volume, opn, close, high, low)
'''

def get_filename_v2_from_item(item):
    filename = os.path.join(item[0], item[1])
    filename = os.path.join(filename, item[2])
    date = time_op.get_date_string_without_padded_zeros(item[3])
    filename = os.path.join(filename, date)
    filename = os.path.join(filename, item[4])
    filename = os.path.join(filename, item[5])
    return filename


'''
def insert_intraday_file_records_v2_into_database(conn, cur, records):
    count = len(records)
    for i in range(count):
        item_count = len(records[i])
        for j in range (item_count):
            item = records[i][j]
            filename = get_filename_v2_from_item(item)
            date_time, volume, opn, close, high, low = read.get_all_intraday_data_from_file(filename)
            suffix_list = get_suffix_list(conn, cur)
            market = item[1]
            symbol_with_suffix = item[2]
            symbol = string_op.get_symbol_without_suffix(symbol_with_suffix, suffix_list)
#            date = time_op.get_date_string_without_padded_zeros(item[3])
#            if read.is_price_list_corrupt(close):
#                add_to_corrupt_intraday_prices(conn, cur, market, symbol, date)
#            else:
            add_to_intraday_prices(conn, cur, market, symbol, date_time, volume, opn, close, high, low)
'''


def get_exchange_names_from_symbol(conn, cursor, symbol):
    names = []
    sql = "SELECT public.stock_exchanges.name from public.stock_exchanges INNER JOIN public.companies ON public.stock_exchanges.exchange_id=public.companies.stock_exchange_id WHERE public.companies.symbol='" + symbol + "';"
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        n = row[0]
        names.append(n)
    return names


def get_exchange_ids_from_symbol(conn, cursor, symbol):
    ids = []
    sql = "SELECT public.companies.stock_exchange_id FROM public.companies WHERE public.companies.symbol='" + symbol + "';"
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        id = row[0]
        ids.append(id)
    return ids


def get_yahoo_suffix_from_exchange_name(conn, cursor, name):
    sql = "SELECT public.stock_exchanges.yahoo_suffix FROM public.stock_exchanges WHERE public.stock_exchanges.name='" + name + "';"
    cursor.execute(sql)
    rows = cursor.fetchall()
    suffix = rows[0][0]
    return suffix


def get_data_v1_exchange_name_from_symbol(conn, cursor, symbol, exchange_dict):
    #because data_v1 doesn't store exchange names, we will add the exchange extension and compare with symbol to find the right market
    if symbol in exchange_dict:
        return exchange_dict[symbol], exchange_dict
    else:
        market = "n_a"
        v1_names = []
        names = get_exchange_names_from_symbol(conn, cursor, symbol)
        for name in names:
            suffix = get_yahoo_suffix_from_exchange_name(conn, cursor, name)
            full_symbol = symbol + suffix
            if (full_symbol == symbol):
                v1_names.append(name)
        if len(v1_names) == 1:
            market = v1_names[0]
            if market == "n/a":
                market = "n_a"
            exchange_dict[symbol] = market
    return market, exchange_dict



def get_raw_intraday_data(conn, cur, market, symbol, start_datetime, end_datetime):
    date_time = []
    volume=[]
    opn = []
    cls = []
    high = []
    low = []

    start_datetime_str = start_datetime.strftime("%Y-%m-%d %H:%M")
    end_datetime_str = end_datetime.strftime("%Y-%m-%d %H:%M")

    sql = "SELECT date_time, volume, opening_price, closing_price, high_price, low_price from public.intraday_prices INNER JOIN public.companies ON public.intraday_prices.company_id=public.companies.company_id \
INNER JOIN public.stock_exchanges ON public.stock_exchanges.exchange_id=public.companies.stock_exchange_id WHERE public.companies.symbol='" + symbol + "' AND public.stock_exchanges.name='" + market + \
"' AND public.intraday_prices.date_time BETWEEN '" + start_datetime_str + "' AND '" + end_datetime_str + "' ORDER BY date_time ASC" +  ";"
    print sql
    cur.execute(sql)
    rows = cur.fetchall()
    count = len(rows)
    if count==0:
        return False, [], [], [], [], [], []
    for row in rows:
        dt = row[0]
        v = row[1]
        o = row[2]
        c = row[3]
        h = row[4]
        l = row[5]
        date_time.append(dt)
        volume.append(float(v))
        opn.append(float(o))
        cls.append(float(c))
        high.append(float(h))
        low.append(float(l))
    return True, date_time, volume, opn, cls, high, low



def get_intraday_data(conn, cur, market, symbol, start_datetime, end_datetime, interval):
    is_data_available, date_time, volume, opn, close, high, low = get_raw_intraday_data(conn, cur, market, symbol, start_datetime, end_datetime)
    if (is_data_available):
        volume, opn, close, high, low, c_v, c_o, c_c, c_h, c_l = heal.heal_intraday_data(volume, opn, close, high, low)
        dtn, vn, on, cn, hn, ln = time_op.get_N_minute_from_one_minute_interval(interval, date_time, volume, opn, close,
                                                                                high, low)
        return (is_data_available, dtn, vn, on, cn, hn, ln, c_v, c_o, c_c, c_h, c_l)
    else:
        return False, [], [], [], [], [], [], 0.0, 0.0, 0.0, 0.0, 0.0



def get_historical_intraday_data_for_N_days(conn, cur, market, symbol, start_datetime, end_datetime, days_count, interval, expected_length):
    date_time_list = []
    volume_per_list = []
    open_per_list = []
    close_per_list = []
    high_per_list = []
    low_per_list = []
    c_v_list = []
    c_o_list = []
    c_c_list = []
    c_h_list = []
    c_l_list = []

    for i in range(1, days_count):
        start_datetime_cur = start_datetime - timedelta(days=i)
        end_datetime_cur = end_datetime - timedelta(days=i)
        is_data_available, date_time, volume, opn, cls, high, low, c_v, c_o, c_c, c_h, c_l = get_intraday_data(conn, cur, market, symbol, start_datetime_cur, end_datetime_cur, interval)
        if not (is_data_available):
            continue

        count = len(date_time)
        if (count != expected_length):
            continue

        date_time_list.append(date_time)
        volume_per_list.append(volume)
        open_per_list.append(opn)
        close_per_list.append(cls)
        high_per_list.append(high)
        low_per_list.append(volume)
        c_v_list.append(c_v)
        c_o_list.append(c_o)
        c_c_list.append(c_c)
        c_h_list.append(c_h)
        c_l_list.append(c_l)
   
    return date_time_list, volume_per_list, open_per_list, close_per_list, high_per_list, low_per_list, c_v_list, c_o_list, c_c_list, c_h_list, c_l_list


 
def get_all_daytimes_for_symbol(conn, cursor, market, symbol):
    date_time_list = []
    sql = "SELECT date_time from public.intraday_prices INNER JOIN public.companies ON public.intraday_prices.company_id=public.companies.company_id \
INNER JOIN public.stock_exchanges ON public.stock_exchanges.exchange_id=public.companies.stock_exchange_id WHERE public.companies.symbol='" + symbol + "' AND public.stock_exchanges.name='" +  market + "';"
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        dt = row[0]
        date_time_list.append(dt)
    return date_time_list



def get_all_days_record_counts(conn, cursor, market, symbol):
    date_time_list = []
    date_record_count = []
    all_daytimes = get_all_daytimes_for_symbol(conn, cursor, market, symbol)
    if len(all_daytimes) == 0:
        return date_time_list, date_record_count
    
    date_time_list.append(time_op.extract_year_month_day(all_daytimes[0]))
    date_record_count.append(0)
    for dt in all_daytimes:
        next_dt = time_op.extract_year_month_day(dt)
        if date_time_list[-1] != next_dt:
            date_time_list.append(next_dt)
            date_record_count.append(1)
        else:
            date_record_count[-1] = date_record_count[-1] + 1

    return date_time_list, date_record_count
    

# This function doesn't work! It takes a very long time and huge amount of memory to call the function! 
# It is better to retrieve all dates by knowing a company (AMZN) that is covered for all dates
def get_all_year_month_day_list(conn, cursor):
    all_times_list = []
    sql = "SELECT date_time from public.intraday_prices;"
    print ("Before executing sql")
    cursor.execute(sql)
    print ("After executing sql")
    rows = cursor.fetchall()
    print ("Fetching all records")
    for row in rows:
        dt_full = row[0]
        dt = time_op.extract_year_month_day(dt_full)
        if dt not in all_times_list:
            all_times_list.append(dt)
            print (all_times_list)
            print ("____________")

    return all_times_list



def get_all_year_month_day_list_for_symbol(conn, cursor, market, symbol):
    all_times_list = []
    date_time_list = get_all_daytimes_for_symbol(conn, cursor, market, symbol)
    for dt_full in date_time_list:
        dt = time_op.extract_year_month_day(dt_full)
        if dt not in all_times_list:
            all_times_list.append(dt)

    return all_times_list

