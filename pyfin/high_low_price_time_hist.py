from read_write import read
from datetime import datetime
from utils import time_op
import numpy as np
from stats import absolute
from viz import histogram


N_minute_interval = 5
neigh_point_count = 5
days_count = 20

start_date = datetime(2018, 1, 4, 9, 30)
end_date = datetime(2018, 1, 4, 15, 59)

max_time_list = []
min_time_list = []

for i in range (days_count):
    new_start_date = time_op.get_date_N_days_ago_from_date(i, start_date)
    new_end_date = time_op.get_date_N_days_ago_from_date(i, end_date)

    is_data_available, date_time, volume , opn, close, high, low = read.get_intraday_data("WEED.TO", new_start_date, new_end_date, "1m")

    if not (is_data_available):
        continue


    date_time_N, volume_N , open_N, close_N, high_N, low_N = absolute.get_N_minute_from_one_minute_interval(N_minute_interval, date_time, volume , opn, close, high, low)


    print "Maximum"
    max_index_list = absolute.get_local_maximum_index_list(close_N, neigh_point_count)
    max_count = len(max_index_list)
    for i in range (max_count):
        print close_N[max_index_list[i]]
        print date_time_N[max_index_list[i]]
        time = datetime(year=2018, month=1, day=1, hour=date_time_N[max_index_list[i]].hour, minute=date_time_N[max_index_list[i]].minute)
        max_time_list.append(time)

    print "Minimum"
    min_index_list = absolute.get_local_minimum_index_list(close_N, neigh_point_count)
    min_count = len(min_index_list)
    for i in range (min_count):
        print close_N[min_index_list[i]]
        print date_time_N[min_index_list[i]]
        time = datetime(year=2018, month=1, day=1, hour=date_time_N[min_index_list[i]].hour, minute=date_time_N[min_index_list[i]].minute)
        min_time_list.append(time)

histogram.show_time_hour_minute_histograpm(max_time_list)
histogram.show_time_hour_minute_histograpm(min_time_list)

