from read_write import read
import numpy as np



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
