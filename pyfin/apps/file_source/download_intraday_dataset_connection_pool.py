import sys
sys.path.append("../..")

import time
from utils import constants
from utils.file_system import read
from utils.db import db
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


#data_root = "/media/hddx/datasets/pyfin/data"
#data_root = "/media/ara/Passport2_4TB/datasets/pyfin/data_v2" 
#data_root = "/media/ara/Passport1_2TB/datasets/pyfin/data_v2"
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


#print (data_root)
#print (N)


if ((data_root is None) or (N is None)):
    print_usage()
    exit()

if not os.path.isdir(data_root):
    print ("Data root must be a valid directory!")
    exit()


conn, cur = db.connect_to_database("../../database/database_settings.txt")

symbols, markets = db.get_all_symbols_and_markets(conn, cur)
#print symbols, markets

cur.close()
conn.close()

connection_pool = None
if (st == constants.Storage_Type.Database):
    threaded_postgreSQL_pool = db.get_connection_pool("../../database/database_settings.txt")

downloader = read.ParallelDownloader(data_root, threaded_postgreSQL_pool, symbols, markets, N, st)
downloader.parallel_download_intraday_list_of_tickers(data_root, symbols, markets, N, st)

if (st == constants.Storage_Type.Database):
    if (threaded_postgreSQL_pool):
        threaded_postgreSQL_pool.closeall
    print("Threaded PostgreSQL connection pool is closed")

seconds = time.time() - start_time

mint, s = divmod(seconds, 60)
h, m = divmod(mint, 60)

print "Elapsed time: %d hours :%02d minutes :%02d seconds" % (h, m, s)


