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



def get_all_symbols(settings_file_name):
    symbols = []
    conn, cursor = connect_to_database(settings_file_name)
#    sql = "SELECT symbol, symbol_suffix FROM public.companies;"
    sql = "SELECT symbol FROM public.companies;"
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        s = row[0]
#temp hack!
#        if row[1] is not None:
#            s = s + row[1]
        symbols.append(s)

    cursor.close()
    conn.close()
    return symbols
