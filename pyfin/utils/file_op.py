from os import listdir
from os.path import isfile, join, isdir
import os
import shutil
import csv

def recreate_new_dir(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)


def ensure_dir_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def if_file_exists(filename):
    if isfile(filename):
        return true
    else:
        return false


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



  

  


