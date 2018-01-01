from read_write import read
from datetime import datetime
import time

N = 365
file_name = "tickers/cannabis.txt"
now = datetime.now()

with open(file_name) as f:
    tickers = f.read().splitlines()

count = len(tickers)

for i in range (count):
    read.get_all_intraday_prices_for_N_days_to_date (tickers[i], N, now)



