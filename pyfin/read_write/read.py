import numpy as np
from numpy import genfromtxt
import pandas_datareader as pdr
from datetime import datetime
import urllib2
import json
import time
import write
import pickle
from datetime import datetime
from os.path import join, isfile
from utils import time_op, string_op, constants
from os.path import join


def get_int_time(date_time):
    date_time_tuple = date_time.timetuple()
    date_time_int = int(time.mktime(date_time_tuple))
    return date_time_int


def get_date_time_from_timestamp(timestamp):
    date_time = []
    count = len(timestamp)
    for i in range(count):
        dt = datetime.fromtimestamp(timestamp[i])
        date_time.append(dt)
    return date_time


def get_intraday_data_from_web(ticker, start, end, interval):
    start_date_time = get_int_time(start)
    end_date_time = get_int_time(end)

    str = "https://query1.finance.yahoo.com/v8/finance/chart/%s?period1=%s&period2=%s&interval=%s" % (ticker, start_date_time, end_date_time, interval)
    response = urllib2.urlopen(str).read()
    json_obj = json.loads(response)

    chart = (json_obj['chart'])
    result = chart['result']
    indicators = result[0]['indicators']
    quote = indicators['quote']

    is_data_available = len(quote[0]) > 0
    if not (is_data_available):
        return (False, [], [], [], [], [], [])
    high = quote[0]['high']
    low = quote[0]['low']
    open = quote[0]['open']
    close = quote[0]['close']
    volume = quote[0]['volume']

    timestamp = result[0]['timestamp']
    date_time = get_date_time_from_timestamp(timestamp)
    return (True, date_time, volume, open, close, high, low)


def get_intraday_data_from_file(full_path, start, end):
    with open(full_path, "rb") as f:
        date_time, volume, opn, close, high, low = pickle.load(f) 
        return (True, date_time, volume, opn, close, high, low)


def get_intraday_data(ticker, start, end, interval):
    dir_name = string_op.get_directory_from_ticker_day_interval(ticker, start, interval)
    filename = string_op.get_filename_from_ticker_day_interval(ticker, start, interval)
    dir_name = join(constants.DATA_ROOT, dir_name)
    full_path = join(dir_name, filename)
    if isfile(full_path):
        return get_intraday_data_from_file(full_path, start, end)
    else:
        is_data_available, date_time, volume, opn, close, high, low = get_intraday_data_from_web("WEED.TO", start, end, interval)
        if (is_data_available):
            write.put_intraday_data_to_file(dir_name, filename, date_time, volume, opn, close, high, low)
        return is_data_available, date_time, volume, opn, close, high, low


def get_data_from_web(ticker, start_date, end_date):
    data = pdr.get_data_yahoo(symbols=ticker, start=start_date, end=end_date)
    dateIndex = data.index
    date = np.array(dateIndex.to_pydatetime())
    return date, data.as_matrix()



def get_all_data_from_file(filename):
    data = genfromtxt(filename, dtype=None, delimiter=',')
    return data


def get_headers_from_all_data(data):
    return data[0]


def get_numeric_data_from_all_data(data):
    return data[1:,1:]


def get_date_from_all_data(data):
    return data[1:,0:1]


def get_date_from_numeric_data(data):
    return data[0:,0:1]


def get_headers_from_file(filename):
    data = get_all_data_from_file(filename)
    return get_headers_from_all_data(data)


def get_numeric_data_from_file(filename):
    data = get_all_data_from_file(filename)
    return get_numeric_data_from_all_data(data)


def get_date_from_file(filename):
    data = get_all_data_from_file(filename)
    return get_date_from_all_data(data)


def get_opening_price_from_numeric_data(data):
    return data[:,0:1].astype(np.float)


def get_high_price_from_numeric_data(data):
    return data[:,1:2].astype(np.float)


def get_low_price_from_numeric_data(data):
    return data[:,2:3].astype(np.float)


def get_closing_price_from_numeric_data(data):
    return data[:,3:4].astype(np.float)


def get_adjusted_closing_price_from_numeric_data(data):
    return data[:,4:5].astype(np.float)


def get_volume_from_numeric_data(data):
    return data[:,5:6].astype(np.float)


def get_opening_price_from_file(filename):
    data = get_numeric_data_from_file(filename)
    return get_opening_price_from_numeric_data(data)


def get_high_price_from_file(filename):
    data = get_numeric_data_from_file(filename)
    return get_high_price_from_numeric_data(data)


def get_low_price_from_file(filename):
    data = get_numeric_data_from_file(filename)
    return get_low_price_from_numeric_data(data)


def get_closing_price_from_file(filename):
    data = get_numeric_data_from_file(filename)
    return get_closing_price_from_numeric_data(data)


def get_adjusted_closing_price_from_file(filename):
    data = get_numeric_data_from_file(filename)
    return get_adjusted_closing_price_from_numeric_data(data)


def get_volume_from_file(filename):
    data = get_numeric_data_from_file(filename)
    return get_volume_from_numeric_data(data)


def get_all_intraday_prices_for_N_days_to_date (ticker, N, last_date):
    date_time_list = []
    volume_list = []
    open_list = []
    close_list = []
    high_list = []
    low_list = []
    for i in range (N):
        date = time_op.get_date_N_days_ago_from_date(i, last_date)

        start_date = date.replace(hour=9, minute=30, second=00)
        end_date = date.replace(hour=16, minute=00, second=00)

        is_data_available, date_time, volume , opn, close, high, low = get_intraday_data(ticker, start_date, end_date, "1m")
        if (is_data_available):
            date_time_list.append(date_time)
            volume_list.append(volume)
            open_list.append(opn)
            close_list.append(close)
            high_list.append(high)
            low_list.append(low)

    return date_time_list, volume_list, open_list, close_list, high_list, low_list


