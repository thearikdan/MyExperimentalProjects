import numpy as np
from numpy import genfromtxt

import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader as pdr

from datetime import datetime
import write
import pickle
from datetime import datetime
from os.path import join, isfile
from utils import time_op, string_op, constants
from utils.web import download
from os.path import join
from utils import constants, heal
from utils.db import db

#https://stackoverflow.com/questions/5442910/python-multiprocessing-pool-map-for-multiple-arguments
import multiprocessing
from functools import partial
from contextlib import contextmanager



def get_all_intraday_data_from_file(full_path):
    with open(full_path, "rb") as f:
        try:
            date_time, volume, opn, close, high, low = pickle.load(f)
            return (date_time, volume, opn, close, high, low)
        except:
            return ([], [], [], [], [], [])



def get_corrupt_ratio(price_list):
    count = len(price_list)
    none_count = 0
    if (count == 0):
        return True

    for i in range (count):
        if heal.is_corrupt_value(price_list[i]):
            none_count = none_count + 1
    none_ratio = float(none_count) / count
    return none_ratio



def is_price_list_corrupt(price_list):
    none_ratio = get_corrupt_ratio(price_list)
    if none_ratio > constants.FILE_CORRUPT_RATIO:
        return True
    else:
        return False


def get_intraday_data_from_file(full_path, start, end):
    with open(full_path, "rb") as f:
        try:
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
        except:         
            return (False, [], [], [], [], [], [])


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

def get_intraday_data(root_dir, symbol_market, start, end, interval, storage_type):
    interval_string = "1m"
    ticker, market = symbol_market.split(":")

    if storage_type == constants.Storage_Type.File_System:
        data_dir = join(root_dir, market)
        dir_name = string_op.get_directory_from_ticker_day_interval(ticker, start, interval_string)
        dir_name = join(data_dir, dir_name)
        filename = string_op.get_filename_from_ticker_day_interval(ticker, start, interval_string)
#    dir_name = join(constants.DATA_ROOT, dir_name)
        full_path = join(dir_name, filename)
        if isfile(full_path):
            is_data_available, date_time, volume, opn, close, high, low = get_intraday_data_from_file(full_path, start, end)
            if (is_data_available):
                volume, opn, close, high, low, c_v, c_o, c_c, c_h, c_l = heal.heal_intraday_data(volume, opn, close, high, low)
                dtn, vn, on, cn, hn, ln = time_op.get_N_units_from_one_unit_interval(interval, date_time, volume, opn, close, high, low)
                return (is_data_available, dtn, vn, on, cn, hn, ln, c_v, c_o, c_c, c_h, c_l)

        is_data_available, date_time, volume, opn, close, high, low = download.get_full_day_intraday_data_from_web(ticker, start, end)
        if not (is_data_available):
            return (False, [], [], [], [], [], [], 0.0, 0.0, 0.0, 0.0, 0.0)

        #Write original data, even if some values are corrupt (0, or None)
        write.put_intraday_data_to_file(dir_name, filename, date_time, volume, opn, close, high, low)

    elif storage_type == constants.Storage_Type.Database:
#        conn, cur = db.connect_to_database("../../database/database_settings.txt")
        is_data_available, dtn, vn, on, cn, hn, ln, c_v, c_o, c_c, c_h, c_l = db.get_intraday_data(market, ticker, start, end, interval)
        if is_data_available:
            return (is_data_available, dtn, vn, on, cn, hn, ln, c_v, c_o, c_c, c_h, c_l)

        is_data_available, date_time, volume, opn, close, high, low = download.get_full_day_intraday_data_from_web(ticker, start, end)
        if not (is_data_available):
            return (False, [], [], [], [], [], [], 0.0, 0.0, 0.0, 0.0, 0.0)

        #Write original data, even if some values are corrupt (0, or None)
        db.add_to_intraday_prices(market, ticker, date_time, volume, opn, close, high, low)
        cur.close()
        conn.close()
    else:
        print("storage type must be file_system or database")
        exit()

    volume, opn, close, high, low, c_v, c_o, c_c, c_h, c_l = heal.heal_intraday_data(volume, opn, close, high, low)

    start_index = date_time.index(start) if start in date_time else None
    end_index = date_time.index(end) if end in date_time else None

    if ((start_index == None) or (end_index == None)):
        return (False, [], [], [], [], [], [], 0.0, 0.0, 0.0, 0.0, 0.0)
    else:
        dt = date_time[start_index:end_index]
        v = volume[start_index:end_index]
        o = opn[start_index:end_index]
        c = close[start_index:end_index]
        h = high[start_index:end_index]
        l = low[start_index:end_index]

        dtn, vn, on, cn, hn, ln = time_op.get_N_minute_from_one_minute_interval(interval, dt, v, o,
                                                                                c, h, l)

        return (True, dtn, vn, on, cn, hn, ln, c_v, c_o, c_c, c_h, c_l)


def download_intraday_data_to_file(data_dir, ticker, start, end):
    interval_string = "1m"
    dir_name = string_op.get_directory_from_ticker_day_interval(ticker, start, interval_string)
    filename = string_op.get_filename_from_ticker_day_interval(ticker, start, interval_string)
    dir_name = join(data_dir, dir_name)
    full_path = join(dir_name, filename)
    if isfile(full_path):
        return True
    else:
        is_data_available, date_time, volume, opn, close, high, low = download.get_full_day_intraday_data_from_web(data_dir, ticker, start, end)
        if not (is_data_available):
            return False

        write.put_intraday_data_to_file(dir_name, filename, date_time, volume, opn, close, high, low)
        return True



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


def get_all_intraday_prices_for_N_days_to_date (data_dir, market_symbol, N, last_date, storage_type):
    #in from_time and to_time only hour, minutes and seconds are important;                                                   years and months are ignored
    date_time_list = []
    volume_list = []
    open_list = []
    close_list = []
    high_list = []
    low_list = []

    ticker, market = market_symbol.split(":")

    start_hour, start_minute = time_op.get_start_time_for_symbol(ticker)
    end_hour, end_minute = time_op.get_end_time_for_symbol(ticker)

    print ("Downloading intraday prices for symbol " + ticker)

    for i in range (N):
        try:
            date = time_op.get_date_N_days_ago_from_date(i, last_date)

            start_date = date.replace(hour=start_hour, minute=start_minute, second=00, microsecond=00)
            end_date = date.replace(hour=end_hour, minute=end_minute, second=00, microsecond=00)

            is_data_available, date_time, volume , opn, close, high, low = get_intraday_data(data_dir, market_symbol, start_date, end_date, 1, storage_type)
            if (is_data_available):
                date_time_list.append(date_time)
                volume_list.append(volume)
                open_list.append(opn)
                close_list.append(close)
                high_list.append(high)
                low_list.append(low)
        except:
            print ("Caught exception in reading data for " + ticker)
            continue

    return date_time_list, volume_list, open_list, close_list, high_list, low_list


def download_all_intraday_prices_for_N_days_to_date (ticker, N, last_date):
    start_hour, start_minute = time_op.get_start_time_for_symbol(ticker)
    end_hour, end_minute = time_op.get_end_time_for_symbol(ticker)

    for i in range (N):
        date = time_op.get_date_N_days_ago_from_date(i, last_date)

        start_date = date.replace(hour=start_hour, minute=start_minute, second=00, microsecond=00)
        end_date = date.replace(hour=end_hour, minute=end_minute, second=00, microsecond=00)

        download_intraday_data(ticker, start_date, end_date)


def download_intraday_list_of_tickers(data_dir, list_file_name, day_count):
    now = datetime.now()
    #in from_time and to_time only hour, minutes and seconds are important; years and months are ignored

    with open(list_file_name) as f:
        tickers = f.read().splitlines()

    count = len(tickers)

    for i in range (count):
        print ("Downloading intraday prices from list " + list_file_name + " for symbol " + tickers[i])
        #download_all_intraday_prices_for_N_days_to_date (tickers[i], day_count, now, from_time, to_time)
        #This method is more thorough because it will also download files that don't have full day data
        get_all_intraday_prices_for_N_days_to_date (data_dir, tickers[i], day_count, now)



def get_historical_intraday_data_for_N_days(data_dir, symbol, start_date, end_date, days_count, interval, expected_length):
    date_time_list = []
    volume_per_list = []
    open_per_list = []
    close_per_list = []
    high_per_list = []
    low_per_list = []

    for i in range (1, days_count):
        new_start_date = time_op.get_date_N_days_ago_from_date(i, start_date)
        new_end_date = time_op.get_date_N_days_ago_from_date(i, end_date)

        is_data_available_before, date_time_before, volume_before , open_before, close_before, high_before, low_before, _, _, _, _, _ = get_intraday_data(data_dir, symbol, new_start_date, new_end_date, interval)
        if not (is_data_available_before):
            continue

        count = len(date_time_before)
        if (count != expected_length):
            continue

        date_time_list.append(date_time_before)
        volume_per_list.append(volume_before)
        open_per_list.append(open_before)
        close_per_list.append(close_before)
        high_per_list.append(high_before)
        low_per_list.append(low_before)

    return date_time_list, volume_per_list, open_per_list, close_per_list, high_per_list, low_per_list 
    



@contextmanager
def poolcontext(*args, **kwargs):
    pool = multiprocessing.Pool(*args, **kwargs)
    yield pool
    pool.terminate()


def merge_params(ticker, args):
    data_dir = args[0]
    day_count = args[1]
    last_date = args[2]
    storage_type = args[3]
#    symbol, market = ticker.split(":")
    market_symbol = ticker
    get_all_intraday_prices_for_N_days_to_date (data_dir, market_symbol, day_count, last_date, storage_type)


def parallel_download_intraday_list_of_tickers(data_dir, tickers, markets, day_count, storage_type):
    #in from_time and to_time only hour, minutes and seconds are important; years and months are ignored
    now = datetime.now()
    # combine tickers with markets to pass param for parallel processing
    count = len(tickers)
    for i in range(count):
        m = markets[i]
        if m =="n/a":
            m = "n_a"
        tickers[i] = tickers[i] + ":" + m

#    tickers = ["AMZN:nasdaq"]

    with poolcontext(processes=multiprocessing.cpu_count()) as pool:

        pool.map(partial(merge_params, args = (data_dir, day_count, now, storage_type)), tickers)



