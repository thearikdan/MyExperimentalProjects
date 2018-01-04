from read_write import read
from datetime import datetime
import time

N = 36
file_name = "tickers/cannabis.txt"
now = datetime.now()

from_time = datetime(2000, 1, 1, 10, 00, 00)
to_time = datetime(2000, 1, 1, 11, 30, 00)
#in from_time and to_time only hour, minutes and seconds are important; years and months are ignored

with open(file_name) as f:
    tickers = f.read().splitlines()

count = len(tickers)

for i in range (count):
    read.get_all_intraday_prices_for_N_days_to_date (tickers[i], N, now, from_time, to_time)



