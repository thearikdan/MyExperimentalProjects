from os import listdir
from os.path import isfile, join, isdir
import os
import shutil
import csv
import time_op

def recreate_new_dir(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)


def ensure_dir_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def if_file_exists(filename):
    if isfile(filename):
        return True
    else:
        return False


def get_only_files(directory): 
    onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]
    return onlyfiles


def get_only_dirs(directory): 
    onlydirs = [f for f in listdir(directory) if isdir(join(directory, f))]
    return onlydirs


def get_nasdaq_downloaded_csv_data(filename):
    symbols = []
    names = []
    last_sales = []
    market_caps = []
    ipo_years = []
    sectors = []
    industries = []
    summary_quotes = []

    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        records = list(reader)

    for rec in records:
        symbols.append(rec[0])
        names.append(rec[1])
        last_sales.append(rec[2])
        market_caps.append(rec[3])
        ipo_years.append(rec[4])
        sectors.append(rec[5])
        industries.append(rec[6])
        summary_quotes.append(rec[7])

    return symbols, names, last_sales, market_caps, ipo_years, sectors, industries, summary_quotes


def get_all_symbols(data_dir):
    return get_only_dirs(data_dir)



def get_hierarchy_list_v1(data_dir):
    items = []

    tickers = get_only_dirs(data_dir)
    ticker_count = len(tickers)

    for i in range (ticker_count):
#    for i in range(10):
        sub_dir = os.path.join(data_dir, tickers[i])
        dates = get_only_dirs(sub_dir)
        date_count = len(dates)
        for j in range(date_count):
            sub_sub_dir = os.path.join(sub_dir, dates[j])
            intervals = get_only_dirs(sub_sub_dir)
            interval_count = len(intervals)
            for k in range(interval_count):
                sub_sub_sub_dir= os.path.join(sub_sub_dir, intervals[k])
                files = get_only_files(sub_sub_sub_dir)
                file_count = len(files)
                for l in range(file_count):
                    item = (data_dir, tickers[i], time_op.convert_date_to_datetime(dates[j]), intervals[k], files[l])
#                        print item
                    items.append((item))
    return items



def get_hierarchy_list_v2(data_dir):
    items = []

    markets = get_only_dirs(data_dir)
    for market in markets:
        market_dir = os.path.join(data_dir, market)
        tickers = get_only_dirs(market_dir)
        ticker_count = len(tickers)

        for i in range (ticker_count):
#    for i in range(10):
            sub_dir = os.path.join(market_dir, tickers[i])
            dates = get_only_dirs(sub_dir)
            date_count = len(dates)
            for j in range(date_count):
                sub_sub_dir = os.path.join(sub_dir, dates[j])
                intervals = get_only_dirs(sub_sub_dir)
                interval_count = len(intervals)
                for k in range(interval_count):
                    sub_sub_sub_dir= os.path.join(sub_sub_dir, intervals[k])
                    files = get_only_files(sub_sub_sub_dir)
                    file_count = len(files)
                    for l in range(file_count):
                        item = (data_dir, market, tickers[i], time_op.convert_date_to_datetime(dates[j]), intervals[k], files[l])
#                        print item
                        items.append((item))
    return items





  

  


