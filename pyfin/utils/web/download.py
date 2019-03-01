from utils import time_op
import urllib2
import json
import pandas_datareader as pdr
import numpy as np


def __get_intraday_data_from_web(ticker, start, end):
    start_date_time = time_op.get_int_time(start)
    end_date_time = time_op.get_int_time(end)

    str = "https://query1.finance.yahoo.com/v8/finance/chart/%s?period1=%s&period2=%s&interval=%s" % (ticker, start_date_time, end_date_time, "1m")
    try:
        response = urllib2.urlopen(str).read()
        json_obj = json.loads(response)

        chart = (json_obj['chart'])
        result = chart['result']
        indicators = result[0]['indicators']
        quote = indicators['quote']

    except Exception as e:
        print "Could not download data for " + ticker + " for " + start.strftime("%Y-%m-%d")
        return (False, [], [], [], [], [], [])

    is_data_available = len(quote[0]) > 0
    if not (is_data_available):
        return (False, [], [], [], [], [], [])

    high = quote[0]['high']
    is_data_available = len(high) > 1
    if not (is_data_available):
        return (False, [], [], [], [], [], [])

    low = quote[0]['low']
    opn = quote[0]['open']
    close = quote[0]['close']
    volume = quote[0]['volume']

    timestamp = result[0]['timestamp']
    date_time = time_op.get_date_time_from_timestamp(timestamp)
    return (True, date_time, volume, opn, close, high, low)


def get_full_day_intraday_data_from_web(ticker, start, end):
    start_full_day = start.replace(hour=9, minute=30, second=00)
    end_full_day = start.replace(hour=16, minute=00, second=00)
    return __get_intraday_data_from_web(ticker, start_full_day, end_full_day)


def get_current_intraday_data_from_web(ticker, start, end):
    start_current_time = start.replace(second=00)
    end_current_time = start.replace(second=00)
    return __get_intraday_data_from_web(ticker, start_current_time, end_current_time)


def get_data_from_web(ticker, start_date, end_date):
    data = pdr.get_data_yahoo(symbols=ticker, start=start_date, end=end_date)
    dateIndex = data.index
    date = np.array(dateIndex.to_pydatetime())
    return date, data.as_matrix()


