import sys
sys.path.append("../..")

import time
from utils import constants
from utils.file_system import read
from utils.db import db, connection_pool
import os 
from argparse import ArgumentParser


def print_usage():
    print ("Usage: python download_intraday_dataset.py -d target directory -n number of days from today -st file_system or database")

parser = ArgumentParser()

parser.add_argument("-d", "--data_root", dest="data_root", help="Specify data root directory")
parser.add_argument("-n", "--day_count", dest="day_count", help="Specify the number of days from today")
parser.add_argument("-st", "--storage_type", dest="storage_type", help="Storage type: file system or database.")


args = parser.parse_args()

params = vars(args)
print (len(sys.argv))

if len(sys.argv) != 7:
    print_usage()
    exit()


start_time = time.time()


data_root = params['data_root']

#N = 1
N= int(params['day_count'])

storage = params['storage_type']
if storage == 'file_system':
    st = constants.Storage_Type.File_System
elif storage == 'database':
    st = constants.Storage_Type.Database
else:
    print ("-st must be file_system or database")
    exit()



if ((data_root is None) or (N is None)):
    print_usage()
    exit()

if not os.path.isdir(data_root):
    print ("Data root must be a valid directory!")
    exit()


conn, cur = db.connect_to_database("../../database/database_settings.txt")

symbols = db.get_all_etf_symbols(conn, cur)
#symbols = ['VXX']
count = len(symbols)
#markets = ['n/a' for i in range(count)]
markets = ['' for i in range(count)]

cur.close()
conn.close()

read.parallel_download_intraday_list_of_tickers(data_root, symbols, markets, N, st, constants.Security_Type.ETF, True)
#read.sequential_download_intraday_list_of_tickers(data_root, symbols, markets, N, st, constants.Security_Type.ETF, True)


seconds = time.time() - start_time

mint, s = divmod(seconds, 60)
h, m = divmod(mint, 60)

print ("Elapsed time: %d hours :%02d minutes :%02d seconds" % (h, m, s))


