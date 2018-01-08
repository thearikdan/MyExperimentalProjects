from read_write import read
from datetime import datetime
from utils import time_op
import matplotlib.pyplot as plt
import numpy as np
from stats import absolute
import matplotlib.ticker as ticker


start_date = datetime(2018, 1, 4, 9, 30)
end_date = datetime(2018, 1, 4, 15, 59)


is_data_available, date_time, volume , opn, close, high, low = read.get_intraday_data("WEED.TO", start_date, end_date, "1m")

if not (is_data_available):
    exit(0)


N = 5

date_time_N, volume_N , open_N, close_N, high_N, low_N = absolute.get_N_minute_from_one_minute_interval(N, date_time, volume , opn, close, high, low)

neigh_point_count = 5

print "Maximum"
max_index_list = absolute.get_local_maximum_index_list(close_N, neigh_point_count)
max_count = len(max_index_list)
for i in range (max_count):
    print close_N[max_index_list[i]]
    print date_time_N[max_index_list[i]]

print "Minimum"
min_index_list = absolute.get_local_minimum_index_list(close_N, neigh_point_count)
min_count = len(min_index_list)
for i in range (min_count):
    print close_N[min_index_list[i]]
    print date_time_N[min_index_list[i]]


plt.plot(date_time_N, close_N)
plt.gcf().autofmt_xdate()


plt.show()
