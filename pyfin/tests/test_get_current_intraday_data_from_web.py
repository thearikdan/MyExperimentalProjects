import sys
sys.path.insert(0, "../")

from read_write import read
from datetime import datetime


start_date = datetime(2018, 2, 6, 9, 30)
end_date = datetime(2018, 2, 6, 10, 30)

is_data_available, date_time, volume , opn, close, high, low = read.get_current_intraday_data_from_web("AMZN", start_date, end_date)

if not (is_data_available):
    exit(0)

print close


