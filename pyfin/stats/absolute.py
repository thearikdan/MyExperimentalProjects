from read_write import read
from utils import constants
import numpy as np
from scipy.signal import argrelextrema


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


def get_N_minute_from_one_minute_interval(N, date_time, volume , opn, close, high, low):
    date_time_N = []
    volume_N = []
    open_N = []
    close_N = []
    high_N = []
    low_N = []
    count = len (date_time)
    if (N > count):
        return date_time_N, volume_N , open_N, close_N, high_N, low_N

    new_count = count / N

    for i in range (new_count):
        date_time_N.append(date_time[N * i])
        volume_N.append(volume[N * i])
        open_N.append(opn[N * i])
        close_N.append(close[N * i])
        high_N.append(max(high[N * i : N * (i + 1)]))
        low_N.append(min(low[N * i : N * (i + 1)]))

    return date_time_N, volume_N , open_N, close_N, high_N, low_N


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

    

