import time
from utils import db, constants
from read_write import read

start_time = time.time()

N = 10

conn, cur = db.connect_to_database("database/database_settings.txt")

#data_root = "/media/hddx/datasets/pyfin/data"
#data_root = "/media/ara/Passport2_4TB/datasets/pyfin/data_v2" 
data_root = "/media/ara/Passport1_2TB/datasets/pyfin/data_v2"

symbols, markets = db.get_all_symbols_and_markets(conn, cur)
print symbols, markets

cur.close()
conn.close()


read.parallel_download_intraday_list_of_tickers(data_root, symbols, markets, N)

seconds = time.time() - start_time

mint, s = divmod(seconds, 60)
h, m = divmod(mint, 60)

print "Elapsed time: %d hours :%02d minutes :%02d seconds" % (h, m, s)
