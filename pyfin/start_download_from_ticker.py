#if during download, just press ctrl-c. It will continue the download.
import time
from utils import db
from read_write import read

start_time = time.clock()

N = 29

last_symbol="NNOMF"

symbols = db.get_all_symbols("database/database_settings.txt")
pos = symbols.index(last_symbol)
symbols = symbols[pos+1:]

#print len(symbols)
#print symbols

read.parallel_download_intraday_list_of_tickers("data", symbols, N)

seconds = time.clock() - start_time

m, s = divmod(seconds, 60)
h, m = divmod(m, 60)
print "Elapsed time: %d hours :%02d minutes :%02d seconds" % (h, m, s)
