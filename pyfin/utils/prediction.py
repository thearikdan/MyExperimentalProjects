from stats import absolute, percentage
from utils import time_op, sort_op, file_op, analytics
from read_write import read
from utils import interpolation
from datetime import datetime, timedelta
from os import path



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
        return ([], [], [], [])

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
    if (count == 0):
        return ([], [], [], [])

    if (top_days_count_to_interpolate > count):
        top_days_count_to_interpolate = count

    interp_volume_per, interp_open_per, interp_close_per, interp_high_per, interp_low_per = interpolation.interpolate_prices_and_volume_by_distance(volume_per_list, open_per_list, close_per_list, high_per_list, low_per_list, dist, top_days_count_to_interpolate)

    predicted_prices = project_percentage_change(last_price, interp_close_per)

    return (predicted_prices, date_time_per_list[0], start[:top_days_count_to_interpolate], dist[:top_days_count_to_interpolate])


def analyse_linear_interpolation_prediction_performance(symbol, start_date, end_date, days_to_analyse, root_dir):
    dir_name = path.join(root_dir, symbol)
    file_op.ensure_dir_exists(dir_name)

    real_start_date = end_date + timedelta(minutes = 1)
    real_end_date = end_date.replace(hour=15, minute=59)

    days_count_list = []
    interp_count_list = []
    distance_list = []

    is_data_available, date_time_real, volume_real, opn_real, close_real, high_real, low_real = read.get_intraday_data(symbol, real_start_date, real_end_date, "1m")

    if not (is_data_available):
        print ("No ground truth data available")
        return

    for i in range (2, days_to_analyse):
        for j in range (1, i):
            predicted_prices, times, closest_date_times, distances = get_linear_interpolation_prediction(symbol, start_date, end_date, i, j)
            distance = analytics.get_distance(close_real, predicted_prices)
        
            days_count_list.append(i)
            interp_count_list.append(j)
            distance_list.append(distance)
        
            info = "Analysed days: %d, Interpolated Closest Days: %d, distance %f\n" % (i, j, distance)
            print info


    sorted_ind = sort_op.get_sorted_indices(distance_list)

    title = "LinearInterpolationPrediction_%s_to_%s.txt" % (start_date.strftime("%Y-%m-%d-%H:%M"), end_date.strftime("%Y-%m-%d-%H:%M"))
    filename = path.join(dir_name, title) 
    f = open(filename, 'w')
    title_str = "Linear Interpolation Prediction for %s from %s to %s\n\n" % (symbol, start_date.strftime("%Y-%m-%d-%H:%M"), end_date.strftime("%Y-%m-%d-%H:%M"))
    f.write(title_str)

    count = len(sorted_ind)
    for i in range (count):
        info = "Analysed days: %d, Interpolated Closest Days: %d, distance %f\n" % (days_count_list[sorted_ind[i]], interp_count_list[sorted_ind[i]], distance_list[sorted_ind[i]])
        f.write(info)

    f.close





