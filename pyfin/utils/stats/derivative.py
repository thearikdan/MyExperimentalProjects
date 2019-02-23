import numpy as np
from utils import time_op, analytics



def get_derivative(start_price, end_price, interval):
    diff = end_price - start_price
    der = diff / interval
    return der


def get_derivative_list(lst, interval):
    der_list = []
    count = len(lst)
    lst_begin = np.array(lst[0:count-1]).astype(float)
    lst_end = np.array(lst[1:count]).astype(float)
    der = get_derivative(lst_begin, lst_end, interval)
    der_list = der.tolist()
    return der_list

'''
def get_percentage_change_in_intraday_prices(date_time, volume , opn, close, high, low):
    count = len(date_time)
    volume_per = get_intraday_percentage_change_in_list(volume)
    open_per = get_intraday_percentage_change_in_list(opn)
    close_per = get_intraday_percentage_change_in_list(close)
    high_per = get_intraday_percentage_change_in_list(high)
    low_per = get_intraday_percentage_change_in_list(low)
    return date_time[1:count], volume_per, open_per, close_per, high_per, low_per
'''

