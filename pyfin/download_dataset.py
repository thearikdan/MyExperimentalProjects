import time
from read_write import read

start_time = time.clock()

N = 36

names = ["tickers/cannabis.txt", "tickers/cannot_be_positive.txt", "tickers/cannot_be_negative.txt", "tickers/battery.txt"]

for name in names:
    read.download_list_of_tickers(name, N)

seconds = time.clock() - start_time

m, s = divmod(seconds, 60)
h, m = divmod(m, 60)
print "Elapsed time: %d:%02d:%02d" % (h, m, s)
