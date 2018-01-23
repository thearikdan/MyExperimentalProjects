from read_write import read
from datetime import datetime
import matplotlib.pyplot as plt
from stats import absolute

start_date = datetime(2017, 12, 28, 10, 30)
end_date = datetime(2017, 12, 28, 11, 30)

is_data_available, date_time, volume , opn, close, high, low = read.get_intraday_data("WEED.TO", start_date, end_date, "1m")

if not (is_data_available):
    exit(0)

N = 2

date_time_N, volume_N , open_N, close_N, high_N, low_N = absolute.get_N_minute_from_one_minute_interval(N, date_time, volume , opn, close, high, low)
print date_time_N
