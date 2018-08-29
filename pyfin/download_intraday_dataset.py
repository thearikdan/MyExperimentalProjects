import time
from utils import db, constants
from read_write import read

start_time = time.clock()

N = 15

conn, cur = db.connect_to_database("database/database_settings.txt")

symbols, markets = db.get_all_symbols_and_markets(conn, cur)
print symbols, markets

cur.close()
conn.close()

read.parallel_download_intraday_list_of_tickers(constants.DATA_ROOT, symbols, markets, N)

seconds = time.clock() - start_time

m, s = divmod(seconds, 60)
h, m = divmod(m, 60)
print "Elapsed time: %d hours :%02d minutes :%02d seconds" % (h, m, s)
