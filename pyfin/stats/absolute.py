from read_write import read
from utils import constants
import numpy as np
from scipy.signal import argrelextrema
from utils import time_op



def get_absolute_change_from_numeric_data(data):
    op = read.get_opening_price_from_numeric_data(data)

    cp = read.get_closing_price_from_numeric_data(data)

    diff = cp - op

    return diff


def get_max_absolute_change_from_numeric_data(data):
    op = read.get_opening_price_from_numeric_data(data)

    hp = read.get_high_price_from_numeric_data(data)

    diff = hp - op

    return diff


def get_min_absolute_change_from_numeric_data(data):
    op = read.get_opening_price_from_numeric_data(data)

    lp = read.get_low_price_from_numeric_data(data)

    diff = lp - op

    return diff


def get_mean_and_deviation_of_day(day_data):
    data = []
    sh = day_data.shape
    for i in range (sh[0]):
        if ((day_data[i] == constants.PADDED_DAY) or (day_data[i] == constants.HOLIDAY)):
            continue
        else:
            data.append(day_data[i])

    data_np = np.array(data)
    mean = np.mean(data_np)
    dev = np.std(data_np)

    return mean, dev


def get_local_maximum_index_list(lst, neighb_point_count):
    np_list = np.array(lst)
    res = argrelextrema(np_list, np.greater, axis=0, order=neighb_point_count)
    indices = []
    count = res[0].size
    for i in range(count):
        indices.append(res[0][i])
    return indices


def get_local_minimum_index_list(lst, neighb_point_count):
    np_list = np.array(lst)
    res = argrelextrema(np_list, np.less, axis=0, order=neighb_point_count)
    indices = []
    count = res[0].size
    for i in range(count):
        indices.append(res[0][i])
    return indices


def get_historical_data(data_dir, symbol, start_date, end_date, days_count):
    date_time_list = []
    volume_per_list = []
    open_per_list = []
    close_per_list = []
    high_per_list = []
    low_per_list = []

    for i in range (1, days_count):
        new_start_date = time_op.get_date_N_days_ago_from_date(i, start_date)
        new_end_date = time_op.get_date_N_days_ago_from_date(i, end_date)

        is_data_available_before, date_time_before, volume_before , open_before, close_before, high_before, low_before = read.get_intraday_data(data_dir, symbol, new_start_date, new_end_date, 1)
        if not (is_data_available_before):
            continue

        date_time_list.append(date_time_before)
        volume_per_list.append(volume_before)
        open_per_list.append(open_before)
        close_per_list.append(close_before)
        high_per_list.append(high_before)
        low_per_list.append(low_before)

    return date_time_list, volume_per_list, open_per_list, close_per_list, high_per_list, low_per_list 
    

