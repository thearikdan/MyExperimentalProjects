import sys
sys.path.append("../..")

import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from utils import time_op, string_op, heal, sort_op
import os
#from utils.file_system import read
from datetime import datetime, timedelta
import math
from utils.stats import percentage
import csv
from threading import Semaphore
from utils.db.connection_pool import Pcursor

'''
class ReallyThreadedConnectionPool(ThreadedConnectionPool):
    def __init__(self, minconn, maxconn, *args, **kwargs):
        self._semaphore = Semaphore(maxconn)
        super().__init__(minconn, maxconn, *args, **kwargs)
#        super(ReallyThreadedConnectionPool, self).__init__(minconn, maxconn, *args, **kwargs)

    def getconn(self, *args, **kwargs):
        self._semaphore.acquire()
        return super().getconn(*args, **kwargs)
#        return super(ReallyThreadedConnectionPool, self).getconn(*args, **kwargs)

    def putconn(self, *args, **kwargs):
        super().putconn(*args, **kwargs)
#        super(ReallyThreadedConnectionPool, self).putconn(*args, **kwargs)
        self._semaphore.release()
'''

g_connection_setting_file_name = None

def set_connection_settings_file_name(name):
    g_connection_setting_file_name = name


def connect_to_database(settings_file_name):
    with open(settings_file_name) as f:
        lines = f.readlines()
    
    #Define our connection string
    conn_string = "host=" + lines[0] + " dbname=" + lines[1] + " user=" + lines[2] + " password=" + lines[3]
 
    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)
 
    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()
    print ("Connected!\n")

    return conn, cursor


'''
def get_connection_pool(settings_file_name):
    threaded_postgreSQL_pool = None

    with open(settings_file_name) as f:
        lines = f.readlines()
    host = lines[0]
    host = "127.0.0.1"
    dbname = lines[1].rstrip()
    user = lines[2].rstrip()
    passwd = lines[3].rstrip()
    
    try:
        threaded_postgreSQL_pool = ReallyThreadedConnectionPool(5, 20, user = user,
                                              password = passwd,
                                              host = host,
                                              database = dbname)
        if(threaded_postgreSQL_pool):
            print("Connection pool created successfully")
        return threaded_postgreSQL_pool

    except (Exception, psycopg2.DatabaseError) as error :
        print ("Error while connecting to PostgreSQL", error)
        exit(0)
'''

'''
#singleton connection pool, gets reset if a connection is bad or drops
_pgpool = None
def pgpool():
    global _pgpool
    if not _pgpool:
        try:

            with open(settings_file_name) as f:
                lines = f.readlines()
            host = lines[0]
            host = "127.0.0.1"
            dbname = lines[1].rstrip()
            user = lines[2].rstrip()
            passwd = lines[3].rstrip()

            _pgpool = ThreadedConnectionPool(5, 20, user = user,
                                              password = passwd,
                                              host = host,
                                              database = dbname)
        except psycopg2.OperationalError as exc:
            _pgpool = None
    return _pgpool
'''

def insert_names(table, conn, cursor, names):
    count = len(names)

    for i in range (count):
        sql = "INSERT INTO " + table +"(name) SELECT('"+names[i]+"') WHERE NOT EXISTS (SELECT * FROM " + table + " WHERE name='"+names[i]+"');"
        #print sql
        try:
            cursor.execute(sql)
        except psycopg2.IntegrityError:
#            print ("SKIPPING " + sql)
            conn.rollback()
        else:
#            print sql
            conn.commit()



def insert_companies(table, conn, cur, symbols, names, ipo_years, sectors, industries, summary_quotes, stock_exchange_ids):
    count = len(names)

    for i in range (count):
        name = names[i].replace("'", "")
        sql = "INSERT INTO " + table +"(symbol, name, ipo_year, sector_id, industry_id, summary_quote, stock_exchange_id) VALUES('" + symbols[i] + "','" + name + "','" + ipo_years[i] + "', (SELECT sector_id from public.sectors WHERE name='" + sectors[i] + "'), (SELECT industry_id from public.industries WHERE name='" + industries[i] + "'), '" + summary_quotes[i] + "', '" + str(stock_exchange_ids[i]) + "');"
        print (sql)
        try:
            cur.execute(sql)
        except psycopg2.IntegrityError:
            print ("SKIPPING " + symbols[i])
            conn.rollback()
        else:
            print ("INSERTNG " + symbols[i])
            conn.commit()


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


def get_all_company_ids(conn, cursor):
    company_ids = []
    sql = "SELECT company_id FROM public.companies;"
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        id = row[0]
        company_ids.append(id)
    return company_ids



def get_company_ids_from_market_and_symbol(market, symbol):
    ids=[]
    exchange_id = get_exchange_id_from_market(market)
    sql = ""
    if exchange_id == None:
        sql ="SELECT company_id FROM public.companies WHERE symbol='" + symbol + "';"
    else:
         sql = "SELECT company_id FROM public.companies WHERE symbol='" + symbol + "' AND stock_exchange_id='"+str(exchange_id)+"';"
    rows = Pcursor().fetchall(sql)
#    cur.execute(sql)
#    rows = cur.fetchall()
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



def get_record_count_in_intraday_prices_for_company_id(conn, cur, company_id):
    sql = "SELECT * FROM public.intraday_prices WHERE (company_id='" + str(company_id) + "');"
    cur.execute(sql)
    rows = cur.fetchall()
    return len(rows)



def if_record_exists_in_intraday_prices_for_company_id(conn, cur, company_id):
    sql = "SELECT EXISTS (SELECT 1 FROM public.intraday_prices WHERE (company_id='" + str(company_id) + "'));"
    cur.execute(sql)
    out = cur.fetchall()
    res = out[0][0]
    return res



def delete_company_id_from_companies(conn, cur, company_id):
    sql = "DELETE FROM public.companies WHERE (company_id='" + str(company_id) + "');"
    try:
        cur.execute(sql)
    except psycopg2.IntegrityError:
        print ("Failed to delete company id " + str(company_id))
        conn.rollback()
    else:
        print ("Deleted company id " + str(company_id))
        conn.commit()


def add_to_corrupt_intraday_prices(conn, cur, market, symbol, date):
    company_ids = get_company_ids_from_market_and_symbol(conn, cur, market, symbol)
    if len(company_ids) != 1:
        return

    sql = "INSERT INTO public.corrupt_intraday_prices (company_id, date) VALUES('" + str(company_ids[0]) + "','" + date + "'::date);"
#    sql = "INSERT INTO public.corrupt_intraday_prices_no_pkey (company_id, date) VALUES('" + str(company_ids[0]) + "','" + date + "'::date);"
    try:
        cur.execute(sql)
    except psycopg2.IntegrityError:
#        print ("SKIPPING " + sql)
        conn.rollback()
    else:
#        print sql
        conn.commit()


def process_numeric_value(val):
    processed = '0'
    if val is None or math.isnan(val):
        processed = 'NaN'
    else:
        processed = str(val)
    return processed


def add_to_intraday_prices(market, symbol, date_time, volume, opn, close, high, low):
    company_ids = get_company_ids_from_market_and_symbol(market, symbol)
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
            Pcursor().execute(sql)
#            cur.execute(sql)
        except psycopg2.IntegrityError:
            print ("SKIPPING " + symbol)
#            conn.rollback()
        else:
            print ("Inserting " + symbol)
#            conn.commit()



def add_to_daily_prices(company_id, date_time, min_volume, min_volume_times, max_volume, max_volume_times, avg_volume, opening, closing, high, high_times, low, low_times, volume_nan_ratio, opening_nan_ratio, closing_nan_ratio, high_nan_ratio, low_nan_ratio):
    date, time = time_op.get_date_time_from_datetime(date_time)
    timestamp = date + " " + time

    min_vo = process_numeric_value(min_volume)
    max_vo = process_numeric_value(max_volume)
    avg_vo = process_numeric_value(avg_volume)
    op = process_numeric_value(opening)
    cl = process_numeric_value(closing)
    hi = process_numeric_value(high)
    lo = process_numeric_value(low)
    vo_nan_r = process_numeric_value(volume_nan_ratio)
    op_nan_r = process_numeric_value(opening_nan_ratio)
    cl_nan_r = process_numeric_value(closing_nan_ratio)
    hi_nan_r = process_numeric_value(high_nan_ratio)
    lo_nan_r = process_numeric_value(low_nan_ratio)

    min_vol_times_str = time_op.get_postgresql_time_array_string(min_volume_times)
    max_vol_times_str = time_op.get_postgresql_time_array_string(max_volume_times)
    high_times_str = time_op.get_postgresql_time_array_string(high_times)
    low_times_str = time_op.get_postgresql_time_array_string(low_times)



    sql = "INSERT INTO public.daily_prices (company_id, date_time, min_volume, min_volume_times, max_volume, max_volume_times, avg_volume, opening_price, closing_price, high_price, high_price_times, low_price, low_price_times, volume_nan_ratio, opening_nan_ratio, closing_nan_ratio, high_nan_ratio, low_nan_ratio)\
 VALUES('" + str(company_id) + "','" + timestamp + "'::timestamp without time zone" + ",'" + min_vo + "'," + min_vol_times_str + ",'" + max_vo + "'," + max_vol_times_str + ",'" +  avg_vo + "','" + op + "','" + cl + "','" + hi + "'," + high_times_str + ",'" + lo + \
          "'," + low_times_str + ",'" + vo_nan_r + "','" + op_nan_r + "','" + cl_nan_r + "','" + hi_nan_r + "','" + lo_nan_r + "');"
#    try:
    Pcursor().execute(sql)
#    except psycopg2.IntegrityError:
#        print ("SKIPPING " + sql)
 #       conn.rollback()
#    else:
    print ("Inserting company " + str(company_id))
#        conn.commit()



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


def get_exchange_id_from_market(market):
    if market == "n_a":
        market = "n/a"
    sql = "SELECT exchange_id FROM public.stock_exchanges WHERE name='" + market + "';"
    rows = Pcursor().fetchall(sql)

#    cursor.execute(sql)
#    rows = cursor.fetchall()
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



#def get_raw_intraday_data(conn, cur, market, symbol, start_datetime, end_datetime):
def get_raw_intraday_data(market, symbol, start_datetime, end_datetime):
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
 #   cur1 = Pcursor()
 #   cir1.execute(sql)
    rows = Pcursor().fetchall(sql)
#    cur.execute(sql)
#    rows = cur.fetchall()
    count = len(rows)
    if count==0: #The danger with this comparison is that if we have incomplete data for the day, it will still return True
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



def get_raw_intraday_data_from_company_id(company_id, start_datetime, end_datetime):
    date_time = []
    volume=[]
    opn = []
    cls = []
    high = []
    low = []

    start_datetime_str = start_datetime.strftime("%Y-%m-%d %H:%M")
    end_datetime_str = end_datetime.strftime("%Y-%m-%d %H:%M")

    sql = "SELECT date_time, volume, opening_price, closing_price, high_price, low_price from public.intraday_prices WHERE company_id='" + str(company_id) + \
"' AND public.intraday_prices.date_time BETWEEN '" + start_datetime_str + "' AND '" + end_datetime_str + "' ORDER BY date_time ASC" +  ";"
#    print sql
#    cur.execute(sql)
#    rows = cur.fetchall()
    rows = Pcursor().fetchall(sql)
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


def get_intraday_data(market, symbol, start_datetime, end_datetime, interval):
    is_data_available, date_time, volume, opn, close, high, low = get_raw_intraday_data(market, symbol, start_datetime, end_datetime)
    if (is_data_available):
        volume, opn, close, high, low, c_v, c_o, c_c, c_h, c_l = heal.heal_intraday_data(volume, opn, close, high, low)
        dtn, vn, on, cn, hn, ln = time_op.get_N_units_from_one_unit_interval(interval, date_time, volume, opn, close,
                                                                                high, low)
        print ("Data are already in database for " + symbol)
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



def get_raw_daily_data(conn, cur, market, symbol, start_datetime, end_datetime):
    date_time = []
    min_volume=[]
    max_volume=[]
    avg_volume=[]
    opn = []
    cls = []
    high = []
    low = []
    volume_nan_ratio = []
    opening_nan_ratio = []
    closing_nan_ratio = []
    high_nan_ratio = []
    low_nan_ratio = []
    min_volume_times = []
    max_volume_times = []
    high_price_times = []
    low_price_times = []


    start_datetime_str = start_datetime.strftime("%Y-%m-%d %H:%M")
    end_datetime_str = end_datetime.strftime("%Y-%m-%d %H:%M")

    sql = "SELECT date_time, min_volume, max_volume, avg_volume, opening_price, closing_price, high_price, low_price, volume_nan_ratio, opening_nan_ratio, closing_nan_ratio, high_nan_ratio, low_nan_ratio, min_volume_times, max_volume_times, high_price_times, low_price_times from public.daily_prices INNER JOIN public.companies ON public.daily_prices.company_id=public.companies.company_id \
INNER JOIN public.stock_exchanges ON public.stock_exchanges.exchange_id=public.companies.stock_exchange_id WHERE public.companies.symbol='" + symbol + "' AND public.stock_exchanges.name='" + market + \
"' AND public.daily_prices.date_time BETWEEN '" + start_datetime_str + "' AND '" + end_datetime_str + "' ORDER BY date_time ASC" +  ";"
#    print sql
    cur.execute(sql)
    rows = cur.fetchall()
    count = len(rows)
    if count==0:
        return False, [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
    for row in rows:
        dt = row[0]
        min_v = row[1]
        max_v = row[2]
        avg_v = row[3]
        o = row[4]
        c = row[5]
        h = row[6]
        l = row[7]
        v_nan_r = row[8]
        o_nan_r = row[9]
        c_nan_r = row[10]
        h_nan_r = row[11]
        l_nan_r = row[12]
        min_v_times = row[13]
        max_v_times = row[14]
        h_times = row[15]
        l_times = row[16]


        date_time.append(dt)
        min_volume.append(float(min_v))
        max_volume.append(float(max_v))
        avg_volume.append(float(avg_v))
        opn.append(float(o))
        cls.append(float(c))
        high.append(float(h))
        low.append(float(l))
        volume_nan_ratio.append(float(v_nan_r))
        opening_nan_ratio.append(float(o_nan_r))
        closing_nan_ratio.append(float(c_nan_r))
        high_nan_ratio.append(float(h_nan_r))
        low_nan_ratio.append(float(l_nan_r))
        min_volume_times.append(str(min_v_times))
        max_volume_times.append(str(max_v_times))
        high_price_times.append(str(h_times))
        low_price_times.append(str(l_times))


    return True, date_time, min_volume, max_volume, avg_volume, opn, cls, high, low, volume_nan_ratio, opening_nan_ratio, closing_nan_ratio, high_nan_ratio, low_nan_ratio, min_volume_times, max_volume_times, high_price_times, low_price_times



def get_day_count(window_count, window_width, stride):
    day_count = window_width + stride * (window_count - 1)
    return day_count




def get_list_by_opening_precentage(conn, cur, symbols, markets, filtered_markets, end_date, day_count, min_price, max_nan_filter):

    count = len(symbols)

    #we'll get data for 2*day_count, and then slice out last day_count to take care of weekends, holidays
    start_date = end_date - timedelta(days=2*day_count)

    date_list = []
    symbol_list = []
    market_list = []
    percentage_opn_list = []
    opn_nan_ratio_list = []
    current_price_list = []

    for i in range(count):
        if markets[i] not in filtered_markets:
            continue
        print("Analysing symbol " + symbols[i] + " on market " + markets[i])
        is_data_available, date_all, min_volume_all, max_volume_all, avg_volume_all, opn_all, cls_all, high_all, low_all, volume_nan_ratio_all, opening_nan_ratio_all, closing_nan_ratio_all, high_nan_ratio_all, low_nan_ratio_all, _, _, _, _ = get_raw_daily_data(
            conn, cur, markets[i], symbols[i], start_date, end_date)
        if not is_data_available:
            continue

        all_count = len(opn_all)

        date = date_all[all_count-day_count:]
        min_volume = min_volume_all[all_count-day_count:]
        max_volume = max_volume_all[all_count-day_count:]
        avg_volume = avg_volume_all[all_count-day_count:]
        opn = opn_all[all_count-day_count:]
        cls = cls_all[all_count-day_count:]
        high = high_all[all_count-day_count:]
        low = low_all[all_count-day_count:]
        volume_nan_ratio = volume_nan_ratio_all[all_count-day_count:]
        opening_nan_ratio = opening_nan_ratio_all[all_count-day_count:]
        closing_nan_ratio = closing_nan_ratio_all[all_count-day_count:]
        high_nan_ratio = high_nan_ratio_all[all_count-day_count:]
        low_nan_ratio = low_nan_ratio_all[all_count-day_count:]

        record_count = len(opn)

        if (opn[record_count - 1] < min_price):
            continue
        pc = percentage.get_percentage_change_in_one_value(opn[0], opn[record_count - 1])
        perc = pc * 100
        nan_ratio = max(opening_nan_ratio[0], opening_nan_ratio[record_count - 1])
        if (nan_ratio > max_nan_filter):
            continue

        date_list.append(date)
        symbol_list.append(symbols[i])
        market_list.append(markets[i])
        percentage_opn_list.append(perc)
        opn_nan_ratio_list.append(nan_ratio)
        current_price_list.append(opn[record_count - 1])

    return date_list, symbol_list, market_list, percentage_opn_list, opn_nan_ratio_list, current_price_list



def get_interday_percentage_change_by_closing_price(conn, cur, symbol, market, start_date, end_date, min_price, max_nan_filter):
    is_data_available, date_all, min_volume_all, max_volume_all, avg_volume_all, opn_all, cls_all, high_all, low_all, volume_nan_ratio_all, opening_nan_ratio_all, closing_nan_ratio_all, high_nan_ratio_all, low_nan_ratio_all, _, _, _, _ = get_raw_daily_data(
        conn, cur, market, symbol, start_date, end_date)
    if not is_data_available:
        return None, None, None, None

    count = len(date_all)
    nan_start = closing_nan_ratio_all[0]
    nan_end = closing_nan_ratio_all[count - 1]
    if ((max_nan_filter < nan_start) or (max_nan_filter < nan_end)):
        return None, None, None, None

    cls_start = cls_all[0]
    cls_end = cls_all[count - 1]
    if (cls_end < min_price):
        return None, None, None, None

    pc = percentage.get_percentage_change_in_one_value(cls_start, cls_end)
    perc = pc * 100
    nan_ratio = max(nan_start, nan_end)
    return perc, cls_start, cls_end, nan_ratio



def get_interday_percentage_change_by_opening_price(conn, cur, symbol, market, start_date, end_date, min_price, max_nan_filter):
    is_data_available, date_all, min_volume_all, max_volume_all, avg_volume_all, opn_all, cls_all, high_all, low_all, volume_nan_ratio_all, opening_nan_ratio_all, closing_nan_ratio_all, high_nan_ratio_all, low_nan_ratio_all, _, _, _, _ = get_raw_daily_data(
        conn, cur, market, symbol, start_date, end_date)
    if not is_data_available:
        return None, None, None, None

    count = len(date_all)
    nan_start = opening_nan_ratio_all[0]
    nan_end = opening_nan_ratio_all[count - 1]
    if ((max_nan_filter < nan_start) or (max_nan_filter < nan_end)):
        return None, None, None, None

    opn_start = opn_all[0]
    opn_end = opn_all[count - 1]
    if (opn_end < min_price):
        return None, None, None, None

    pc = percentage.get_percentage_change_in_one_value(opn_start, opn_end)
    perc = pc * 100
    nan_ratio = max(nan_start, nan_end)
    return perc, opn_start, opn_end, nan_ratio


def get_sorted_ascending_trend_by_opening_precentage(conn, cur, filtered_markets, end_date, window_count, window_width, stride, min_price, max_nan_filter):

    symbols, markets = get_all_symbols_and_markets(conn, cur)
    day_count = get_day_count(window_count, window_width, stride)


    date_list_resorted_list = []
    symbol_list_resorted_list = []
    market_list_resorted_list = []
    percentage_opn_list_resorted_list = []
    opn_nan_ratio_list_resorted_list = []
    current_price_list_resorted_list = []

    #get dates that we will need to iterate through from amazon
    date_list, _, _, _, _, _ = get_list_by_opening_precentage(
        conn, cur, symbols, markets, filtered_markets, end_date, day_count, min_price,
        max_nan_filter)

    for i in range (window_count):
        date_list, symbol_list, market_list, percentage_opn_list, opn_nan_ratio_list, current_price_list = get_list_by_opening_precentage(
            conn, cur, symbols, markets, filtered_markets, end_date, day_count, min_price,
            max_nan_filter)

        sorted_indices = sort_op.get_sorted_indices(percentage_opn_list[stride * i : stride * i + window_width])
        date_list_resorted = sort_op.get_resorted_list(date_list[stride * i : stride * i + window_width], sorted_indices)
        symbol_list_resorted = sort_op.get_resorted_list(symbol_list[stride * i : stride * i + window_width], sorted_indices)
        market_list_resorted = sort_op.get_resorted_list(market_list[stride * i : stride * i + window_width], sorted_indices)
        percentage_opn_list_resorted = sort_op.get_resorted_list(percentage_opn_list[stride * i : stride * i + window_width], sorted_indices)
        opn_nan_ratio_list_resorted = sort_op.get_resorted_list(opn_nan_ratio_list[stride * i : stride * i + window_width], sorted_indices)
        current_price_list_resorted = sort_op.get_resorted_list(current_price_list[stride * i : stride * i + window_width], sorted_indices)

        date_list_resorted_list.append(date_list_resorted)
        symbol_list_resorted_list.append(symbol_list_resorted)
        market_list_resorted_list.append(market_list_resorted)
        percentage_opn_list_resorted_list.append(percentage_opn_list_resorted)
        opn_nan_ratio_list_resorted_list.append(opn_nan_ratio_list_resorted)
        current_price_list_resorted_list.append(current_price_list_resorted)


    return date_list_resorted_list, symbol_list_resorted_list, market_list_resorted_list, percentage_opn_list_resorted_list, opn_nan_ratio_list_resorted_list, current_price_list_resorted_list


def get_tickers_from_yahoo_csv(csv_file):
    tickers = []
    with open(csv_file) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
             tickers.append(row[0])
    tickers.pop(0) # remove top
    return tickers



def get_from_target_exchanges(exch, target_exchanges):
    for e in exch:
        if e in target_exchanges:
            return e
    return ''


def filter_by_target_exchanges(all_symbols, all_exchanges, target_exchanges):
    symbols = []
    exchanges = []
    count = len(all_exchanges)
    for i in range (count):
        if not (all_exchanges[i] in target_exchanges):
            continue
        symbols.append(all_symbols[i])
        exchanges.append(all_exchanges[i])
    return symbols, exchanges
        

def get_symbols_and_exchanges_from_yahoo_csv(conn, cursor, csv_file, target_exchanges):
    symbols = []
    exchanges = []

    all_symbols = get_tickers_from_yahoo_csv(csv_file)
    for symbol in all_symbols:
        exch = get_exchange_names_from_symbol(conn, cursor, symbol)
        target_ex = get_from_target_exchanges(exch, target_exchanges)
        if len(target_ex) == 0:
            continue
        symbols.append(symbol)
        exchanges.append(target_ex)

    return symbols, exchanges


