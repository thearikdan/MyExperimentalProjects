import sys
sys.path.insert(0, "../")

from read_write import read
from datetime import datetime


start_date = datetime(2018, 2, 6, 9, 30)
end_date = datetime(2018, 2, 6, 15, 39)

is_data_available, date_time, volume , opn, close, high, low = read.get_intraday_data("AMZN", start_date, end_date, 1)

if not (is_data_available):
    exit(0)

print close

