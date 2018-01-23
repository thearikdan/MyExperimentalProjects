from read_write import read
from datetime import datetime
import matplotlib.pyplot as plt
from stats import percentage, absolute
from utils import analytics, time_op, sort_op
import numpy as np
from viz import vertical_plots


start_date = datetime(2018, 1, 22, 9, 30)
end_date = datetime(2018, 1, 22, 10, 30)

days_count = 18

symbol = "WEED.TO"
#symbol = "EMHTF"
#symbol = "PRMCF"
#symbol = "ACBFF"
#symbol = "MEDFF"
#symbol = "AMZN"


def get_closest_distance_time_to_predict_and_distance(symbol, start_date, end_date, days_count):
    date_time, date_time_per_list, _, _, (close, close_per, close_per_list, dist_close_per_list), _, _ = percentage.get_percentage_change_distance_data(symbol, start_date, end_date, days_count)

    date_time_list, volume_list, open_list, close_list, high_list, low_list = absolute.get_historical_data(symbol, start_date, end_date, days_count)

    sorted_ind = sort_op.get_sorted_indices(dist_close_per_list)


    resorted_date_time_per_list = sort_op.get_resorted_list(date_time_per_list, sorted_ind)
    resorted_close_per_list = sort_op.get_resorted_list(close_per_list, sorted_ind)

    time_count = len(resorted_date_time_per_list[0])
    closest_start_time, closest_end_time = time_op.get_date_time_interval_until_end_of_day(resorted_date_time_per_list[0][time_count -1 ], end_date)

    closest_distance = dist_close_per_list[sorted_ind[0]]
    return (closest_start_time, closest_end_time, closest_distance)

start, end, dist = get_closest_distance_time_to_predict_and_distance(symbol, start_date, end_date, days_count)
print start, end, dist

