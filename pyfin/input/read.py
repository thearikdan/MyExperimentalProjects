import numpy as np
from numpy import genfromtxt
import pandas_datareader as pdr
from datetime import datetime
import urllib2
import json
import time
from datetime import datetime


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

    high = quote[0]['high']
    low = quote[0]['low']
    open = quote[0]['open']
    close = quote[0]['close']
    volume = quote[0]['volume']

    timestamp = result[0]['timestamp']
    date_time = get_date_time_from_timestamp(timestamp)
    return date_time, volume, open, close, high, low


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


