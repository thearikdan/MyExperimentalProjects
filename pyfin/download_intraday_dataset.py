import time
from read_write import read

start_time = time.clock()

N = 14

names = ["tickers/cannabis.txt", "tickers/cannot_be_positive.txt", "tickers/cannot_be_negative.txt", "tickers/battery.txt", "tickers/nasdaqlisted_full.txt", "tickers/otherlisted.txt"]

#names = ["tickers/otherlisted.txt"]


for name in names:
    read.download_intraday_list_of_tickers(name, N)

seconds = time.clock() - start_time

m, s = divmod(seconds, 60)
h, m = divmod(m, 60)
print "Elapsed time: %d hours :%02d minutes :%02d seconds" % (h, m, s)
