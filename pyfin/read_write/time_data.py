from utils import time_op
import read
from stats import absolute
from datetime import datetime


def get_high_and_low_price_times(symbol, start_date, end_date, days_count, N_minute_interval, neighb_point_count):
    max_time_list = []
    min_time_list = []

    for i in range (days_count):
        new_start_date = time_op.get_date_N_days_ago_from_date(i, start_date)
        new_end_date = time_op.get_date_N_days_ago_from_date(i, end_date)

        is_data_available, date_time, volume , opn, close, high, low = read.get_intraday_data(symbol, new_start_date, new_end_date, "1m")

        if not (is_data_available):
            continue

        date_time_N, volume_N , open_N, close_N, high_N, low_N = absolute.get_N_minute_from_one_minute_interval(N_minute_interval, date_time, volume , opn, close, high, low)

        max_index_list = absolute.get_local_maximum_index_list(close_N, neighb_point_count)
        max_count = len(max_index_list)
        for i in range (max_count):
            time = datetime(year=2018, month=1, day=1, hour=date_time_N[max_index_list[i]].hour, minute=date_time_N[max_index_list[i]].minute)
            max_time_list.append(time)

        min_index_list = absolute.get_local_minimum_index_list(close_N, neighb_point_count)
        min_count = len(min_index_list)
        for i in range (min_count):
            time = datetime(year=2018, month=1, day=1, hour=date_time_N[min_index_list[i]].hour, minute=date_time_N[min_index_list[i]].minute)
            min_time_list.append(time)

    return max_time_list, min_time_list

