from stats import absolute, percentage
from utils import time_op, sort_op
from read_write import read
from utils import interpolation


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



def get_linear_interpolation_prediction(symbol, from_date_time, to_date_time, days_count_to_analyse, top_days_count_to_interpolate):
    
    is_data_available, date_time_curr, volume_curr , opn_curr, close_curr, high_curr, low_curr = read.get_intraday_data(symbol, from_date_time, to_date_time, "1m")

    if not (is_data_available):
        return None

    count_curr = len(close_curr)
    last_price = close_curr[count_curr - 1]

    start, end, dist = get_closest_distances_time_to_predict_and_distances(symbol, from_date_time, to_date_time, days_count_to_analyse)

    count = len(start)

    date_time_per_list = []
    volume_per_list = []
    open_per_list = []
    close_per_list = []
    high_per_list = []
    low_per_list = []

    for i in range (count):
        is_data_available, date_time, volume , opn, close, high, low = read.get_intraday_data(symbol, start[i], end[i], "1m")
        
        if not (is_data_available):
            continue

        date_time_per, volume_per, open_per, close_per, high_per, low_per = percentage.get_percentage_change_in_intraday_prices(date_time, volume , opn, close, high, low)

        date_time_per_list.append(date_time_per)
        volume_per_list.append(volume_per)
        open_per_list.append(open_per)
        close_per_list.append(close_per)
        high_per_list.append(high_per)
        low_per_list.append(low_per)

    count = len(date_time_per_list)

    if (top_days_count_to_interpolate > count):
        top_days_count_to_interpolate = count

    interp_volume_per, interp_open_per, interp_close_per, interp_high_per, interp_low_per = interpolation.interpolate_prices_and_volume_by_distance(volume_per_list, open_per_list, close_per_list, high_per_list, low_per_list, dist, top_days_count_to_interpolate)

    predicted_prices = project_percentage_change(last_price, interp_close_per)

    return (predicted_prices, date_time_per_list[0], start[:top_days_count_to_interpolate], dist[:top_days_count_to_interpolate])


