from utils.read_write import read
import numpy as np
from utils import time_op, analytics



def get_percentage_change(start_price, end_price):
    diff = end_price - start_price
    per = diff / start_price
    return per


def get_intraday_percentage_change(lst):
    count = len(lst)
    lst_begin = np.array(lst[0:count-1]).astype(float)
    lst_end = np.array(lst[1:count]).astype(float)
    #Some of the element of list_begin can be 0 (first minute volume, for example)
    #To avoid dividing by 0, we'll replace all 0-es by 1
    for i in range (count - 1):
        if (lst_begin[i] == 0):
            lst_begin[i] = 1
    perc = (lst_end - lst_begin) / lst_begin
    perc_list = perc.tolist()
    return perc_list


def get_percentage_change_in_intraday_prices(date_time, volume , opn, close, high, low):
    count = len(date_time)
    volume_per = get_intraday_percentage_change(volume)
    open_per = get_intraday_percentage_change(opn)
    close_per = get_intraday_percentage_change(close)
    high_per = get_intraday_percentage_change(high)
    low_per = get_intraday_percentage_change(low)
    return date_time[1:count], volume_per, open_per, close_per, high_per, low_per


def get_historical_percentage_data(data_dir, symbol, start_date, end_date, days_count):
    date_time_list = []
    volume_per_list = []
    open_per_list = []
    close_per_list = []
    high_per_list = []
    low_per_list = []

    for i in range (1, days_count):
        new_start_date = time_op.get_date_N_days_ago_from_date(i, start_date)
        new_end_date = time_op.get_date_N_days_ago_from_date(i, end_date)

        is_data_available_before, date_time_before, volume_before , opn_before, close_before, high_before, low_before = read.get_intraday_data(data_dir, symbol, new_start_date, new_end_date, 1)
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




