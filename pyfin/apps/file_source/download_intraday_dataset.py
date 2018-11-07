import sys
sys.path.append("../..")

import time
from utils import constants
from utils.file_system import read
from utils.db import db
import os 
from argparse import ArgumentParser


def print_usage():
    print"Usage: python download_intraday_dataset.py -d target_directory -n number_of_days_from_today"

parser = ArgumentParser()

parser.add_argument("-d", "--data_root", dest="data_root", help="Specify data root directory")
parser.add_argument("-n", "--day_count", dest="day_count", help="Specify the number of days from today")


args = parser.parse_args()

params = vars(args)
print len(sys.argv)

if len(sys.argv) != 5:
    print_usage()
    exit()


start_time = time.time()


#data_root = "/media/hddx/datasets/pyfin/data"
#data_root = "/media/ara/Passport2_4TB/datasets/pyfin/data_v2" 
#data_root = "/media/ara/Passport1_2TB/datasets/pyfin/data_v2"
data_root = params['data_root']

#N = 1
N= int(params['day_count'])

#print (data_root)
#print (N)


if ((data_root is None) or (N is None)):
    print_usage()
    exit()

if not os.path.isdir(data_root):
    print"Data root must be a valid directory!"
    exit()


conn, cur = db.connect_to_database("../../database/database_settings.txt")

symbols, markets = db.get_all_symbols_and_markets(conn, cur)
print symbols, markets

cur.close()
conn.close()


read.parallel_download_intraday_list_of_tickers(data_root, symbols, markets, N)

seconds = time.time() - start_time

mint, s = divmod(seconds, 60)
h, m = divmod(mint, 60)

print "Elapsed time: %d hours :%02d minutes :%02d seconds" % (h, m, s)

