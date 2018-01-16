from read_write import read
import numpy as np
from utils import time_op



def get_percentage_change_from_numeric_data(data):
    op = read.get_opening_price_from_numeric_data(data)
    cp = read.get_closing_price_from_numeric_data(data)
    diff = cp - op
    per = diff / op
    return per


def get_high_opening_percentage_change_from_numeric_data(data):
    op = read.get_opening_price_from_numeric_data(data)
    hp = read.get_high_price_from_numeric_data(data)
    diff = hp - op
    per = diff / op
    return per


def get_low_opening_percentage_change_from_numeric_data(data):
    op = read.get_opening_price_from_numeric_data(data)
    lp = read.get_low_price_from_numeric_data(data)
    diff = lp - op
    per = diff / op
    return per


def get_high_low_percentage_change_from_numeric_data(data):
    hp = read.get_high_price_from_numeric_data(data)
    lp = read.get_low_price_from_numeric_data(data)
    diff = hp - lp
    per = diff / lp
    return per


def get_intraday_percentage_change(list):
    count = len(list)
    list_begin = np.array(list[0:count-1]).astype(float)
    list_end = np.array(list[1:count]).astype(float)
    #Some of the element of list_begin can be 0 (first minute volume, for example)
    #To avoid dividing by 0, we'll replace all 0-es by 1
    for i in range (count - 1):
        if (list_begin[i] == 0):
            list_begin[i] = 1
    perc = (list_end - list_begin) / list_begin
    return perc


def get_percentage_change_in_intraday_prices(date_time, volume , opn, close, high, low):
    count = len(date_time)
    volume_per = get_intraday_percentage_change(volume)
    open_per = get_intraday_percentage_change(opn)
    close_per = get_intraday_percentage_change(close)
    high_per = get_intraday_percentage_change(high)
    low_per = get_intraday_percentage_change(low)
    return date_time[1:count], volume_per, open_per, close_per, high_per, low_per


def get_historical_percentage_data(symbol, start_date, end_date, days_count):
    date_time_list = []
    volume_per_list = []
    open_per_list = []
    close_per_list = []
    high_per_list = []
    low_per_list = []

    for i in range (1, days_count):
        new_start_date = time_op.get_date_N_days_ago_from_date(i, start_date)
        new_end_date = time_op.get_date_N_days_ago_from_date(i, end_date)

        is_data_available_before, date_time_before, volume_before , opn_before, close_before, high_before, low_before = read.get_intraday_data(symbol, new_start_date, new_end_date, "1m")
        if not (is_data_available_before):
            continue

        date_time_per_before, volume_per_before , open_per_before, close_per_before, high_per_before, low_per_before = get_percentage_change_in_intraday_prices(date_time_before, volume_before , opn_before, close_before, high_before, low_before)

        date_time_list.append(date_time_per_before)
        volume_per_list.append(volume_per_before)
        open_per_list.append(open_per_before)
        close_per_list.append(close_per_before)
        high_per_list.append(high_per_before)
        low_per_list.append(low_per_before)

    return date_time_list, volume_per_list, open_per_list, close_per_list, high_per_list, low_per_list 

