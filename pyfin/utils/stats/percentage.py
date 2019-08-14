import numpy as np
from utils import time_op, analytics



def get_percentage_change_in_one_value(start_price, end_price):
    diff = end_price - start_price
    per = diff / start_price
    return per


def get_percentage_change_in_list(lst):
    count = len(lst)
    lst_begin = np.array(lst[0:count-1]).astype(float)
    lst_end = np.array(lst[1:count]).astype(float)
    #Some of the element of list_begin can be 0 (first minute volume, for example)
    #To avoid dividing by 0, we'll replace all 0-es by neighbouring value or 1
    for i in range (count - 1):
        if (lst_begin[i] == 0):
            if ((i + 1) < (count - 1) and (lst_begin[i + 1] != 0)):
                lst_begin[i] = lst_begin[i + 1]
            elif ((i - 1) >= 0 and (lst_begin[i - 1] != 0)):
                lst_begin[i] = lst_begin[i - 1]
            else:
                lst_begin[i] = 1
    perc = get_percentage_change_in_one_value(lst_begin, lst_end)
    perc_list = perc.tolist()
    return perc_list


def get_percentage_change_in_intraday_prices(date_time, volume , opn, close, high, low):
    count = len(date_time)
    volume_per = get_percentage_change_in_list(volume)
    open_per = get_percentage_change_in_list(opn)
    close_per = get_percentage_change_in_list(close)
    high_per = get_percentage_change_in_list(high)
    low_per = get_percentage_change_in_list(low)
    return date_time[1:count], volume_per, open_per, close_per, high_per, low_per


