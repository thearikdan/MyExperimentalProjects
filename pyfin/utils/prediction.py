from stats import absolute, percentage
from utils import time_op, sort_op



def get_closest_distances_time_to_predict_and_distances(symbol, start_date, end_date, days_count):
    date_time, date_time_per_list, _, _, (close, close_per, close_per_list, dist_close_per_list), _, _ = percentage.get_percentage_change_distance_data(symbol, start_date, end_date, days_count)

    sorted_ind = sort_op.get_sorted_indices(dist_close_per_list)

    resorted_date_time_per_list = sort_op.get_resorted_list(date_time_per_list, sorted_ind)

    closest_start_time_list = []
    closest_end_time_list = []
    closest_distance_list = []

    count = len (resorted_date_time_per_list)

    for i in range (count):
        time_count = len(resorted_date_time_per_list[i])
        closest_start_time, closest_end_time = time_op.get_date_time_interval_until_end_of_day(resorted_date_time_per_list[i][time_count -1 ], end_date)
        closest_distance = dist_close_per_list[sorted_ind[i]]

        closest_start_time_list.append(closest_start_time)
        closest_end_time_list.append(closest_end_time)
        closest_distance_list.append(closest_distance)

    return (closest_start_time_list, closest_end_time_list, closest_distance_list)



def project_percentage_change(num, percentage_list):
    count = len (percentage_list)

    proj = []
    b = num

    for i in range (count):
        b = b * (1 + percentage_list[i])
        proj.append(b)

    return proj
