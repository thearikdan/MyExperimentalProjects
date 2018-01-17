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
    #always get full day data from web
    start_full_day = start.replace(hour=9, minute=30, second=00)
    end_full_day = start.replace(hour=16, minute=00, second=00)
    start_date_time = get_int_time(start_full_day)
    end_date_time = get_int_time(end_full_day)

    str = "https://query1.finance.yahoo.com/v8/finance/chart/%s?period1=%s&period2=%s&interval=%s" % (ticker, start_date_time, end_date_time, interval)
    try:
        response = urllib2.urlopen(str).read()
        json_obj = json.loads(response)
    except Exception as e:
        return (False, [], [], [], [], [], [])

    chart = (json_obj['chart'])
    result = chart['result']
    indicators = result[0]['indicators']
    quote = indicators['quote']

    is_data_available = len(quote[0]) > 0
    if not (is_data_available):
        return (False, [], [], [], [], [], [])

    high = quote[0]['high']
    is_data_available = len(high) > 1
    if not (is_data_available):
        return (False, [], [], [], [], [], [])

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
        start_index = date_time.index(start) if start in date_time else None
        end_index = date_time.index(end) if end in date_time else None

        if ((start_index == None) or (end_index == None)):
            return (False, [], [], [], [], [], [])
        else:
            return (True,
                date_time[start_index:end_index],
                volume[start_index:end_index],
                opn[start_index:end_index],
                close[start_index:end_index],
                high[start_index:end_index],
                low[start_index:end_index])


def is_corrupt_value(a):
    if (a == 0) or (a is None):
        return True
    else:
        return False


def find_next_good_value(lst, index):
    val = None
    count = len(lst)

    if (index >= count):
        return val

    for i in range(index + 1, count):
        if not is_corrupt_value(lst[i]):
            val = lst[i]
            return val
    return val


def find_previous_good_value(lst, index):
    val = None
    count = len(lst)

    if (index >= count):
        return val

    if (index <= 0):
        return val

    for i in range(0, index - 1):
        if not is_corrupt_value(lst[i]):
            val = lst[i]
            return val
    return val


def heal_list(lst):
    count = len(lst)
    for i in range(count):
        if is_corrupt_value(lst[i]):
            lst[i] = find_next_good_value(lst, i)
            if (lst[i] is None):
                lst[i] = find_previous_good_value(lst, i)
    return lst


def heal_intraday_data(volume, opn, close, high, low):
    v = heal_list(volume)
    o = heal_list(opn)
    c = heal_list(close)
    h = heal_list(high)
    l = heal_list(low)
    return (v, o, c, h, l)

'''
def delete_element(date_time, volume, opn, close, high, low, index):
    del date_time[index]
    del volume[index]
    del opn[index]
    del close[index]
    del high[index]
    del low[index]
    return date_time, volume, opn, close, high, low

#although removing None element is a cleaner solution, the problem is that we want to keep the length for all days to be the same
#therefore we will put neighboring values into corrupted positions

def heal_intraday_data(date_time, volume, opn, close, high, low):
    res = True
    if (None in volume):
        ind = volume.index(None)
        date_time, volume, opn, close, high, low = delete_element(date_time, volume, opn, close, high, low, ind)
        res = False
    if (None in opn):
        ind = volume.opn(None)
        date_time, volume, opn, close, high, low = delete_element(date_time, volume, opn, close, high, low, ind)
        res = False
    if (None in close):
        ind = close.index(None)
        date_time, volume, opn, close, high, low = delete_element(date_time, volume, opn, close, high, low, ind)
        res = False
    if (None in high):
        ind = high.index(None)
        date_time, volume, opn, close, high, low = delete_element(date_time, volume, opn, close, high, low, ind)
        res = False
    if (None in close):
        ind = close.index(None)
        date_time, volume, opn, close, high, low = delete_element(date_time, volume, opn, close, high, low, ind)
        res = False
    if not (res):
        return heal_intraday_data(date_time, volume, opn, close, high, low)
    else:
        return date_time, volume, opn, close, high, low
'''

def get_intraday_data(ticker, start, end, interval):
    dir_name = string_op.get_directory_from_ticker_day_interval(ticker, start, interval)
    filename = string_op.get_filename_from_ticker_day_interval(ticker, start, interval)
    dir_name = join(constants.DATA_ROOT, dir_name)
    full_path = join(dir_name, filename)
    if isfile(full_path):
        is_data_available, date_time, volume, opn, close, high, low = get_intraday_data_from_file(full_path, start, end)
        if (is_data_available):
            volume, opn, close, high, low = heal_intraday_data(volume, opn, close, high, low)
            return (is_data_available, date_time, volume, opn, close, high, low)

    is_data_available, date_time, volume, opn, close, high, low = get_intraday_data_from_web(ticker, start, end, interval)
    if not (is_data_available):
        return (False, [], [], [], [], [], [])

    #Write original data, even if some values are corrupt (0, or None)
    write.put_intraday_data_to_file(dir_name, filename, date_time, volume, opn, close, high, low)

    volume, opn, close, high, low = heal_intraday_data(volume, opn, close, high, low)

    start_index = date_time.index(start) if start in date_time else None
    end_index = date_time.index(end) if end in date_time else None

    if ((start_index == None) or (end_index == None)):
        return (False, [], [], [], [], [], [])
    else:
        return (True,
            date_time[start_index:end_index],
            volume[start_index:end_index],
            opn[start_index:end_index],
            close[start_index:end_index],
            high[start_index:end_index],
            low[start_index:end_index])


def download_intraday_data(ticker, start, end, interval):
    dir_name = string_op.get_directory_from_ticker_day_interval(ticker, start, interval)
    filename = string_op.get_filename_from_ticker_day_interval(ticker, start, interval)
    dir_name = join(constants.DATA_ROOT, dir_name)
    full_path = join(dir_name, filename)
    if isfile(full_path):
        return True
    else:
        is_data_available, date_time, volume, opn, close, high, low = get_intraday_data_from_web(ticker, start, end, interval)
        if not (is_data_available):
            return False

        write.put_intraday_data_to_file(dir_name, filename, date_time, volume, opn, close, high, low)
        return True


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


def get_all_intraday_prices_for_N_days_to_date (ticker, N, last_date, from_time, to_time):
    #in from_time and to_time only hour, minutes and seconds are important;                                                   years and months are ignored
    date_time_list = []
    volume_list = []
    open_list = []
    close_list = []
    high_list = []
    low_list = []
    for i in range (N):
        date = time_op.get_date_N_days_ago_from_date(i, last_date)

        start_date = date.replace(hour=from_time.hour, minute=from_time.minute, second=00, microsecond=00)
        end_date = date.replace(hour=to_time.hour, minute=to_time.minute, second=00, microsecond=00)

        is_data_available, date_time, volume , opn, close, high, low = get_intraday_data(ticker, start_date, end_date, "1m")
        if (is_data_available):
            date_time_list.append(date_time)
            volume_list.append(volume)
            open_list.append(opn)
            close_list.append(close)
            high_list.append(high)
            low_list.append(low)

    return date_time_list, volume_list, open_list, close_list, high_list, low_list


def download_all_intraday_prices_for_N_days_to_date (ticker, N, last_date, from_time, to_time):
    for i in range (N):
        date = time_op.get_date_N_days_ago_from_date(i, last_date)

        start_date = date.replace(hour=from_time.hour, minute=from_time.minute, second=00, microsecond=00)
        end_date = date.replace(hour=to_time.hour, minute=to_time.minute, second=00, microsecond=00)

        download_intraday_data(ticker, start_date, end_date, "1m")

def download_list_of_tickers(list_file_name, day_count):
    now = datetime.now()
    from_time = datetime(2000, 1, 1, 9, 30, 00)
    to_time = datetime(2000, 1, 1, 15, 59, 00)
    #in from_time and to_time only hour, minutes and seconds are important; years and months are ignored

    with open(list_file_name) as f:
        tickers = f.read().splitlines()

    count = len(tickers)

    for i in range (count):
        print "Downloading intraday prices from list " + list_file_name + " for symbol " + tickers[i]
        download_all_intraday_prices_for_N_days_to_date (tickers[i], day_count, now, from_time, to_time)




