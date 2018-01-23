from datetime import datetime
from utils import prediction
from stats import percentage
from read_write import read


def interpolate_by_distance(my_list, dist, interp_count):
    list_count = len(my_list)
    dist_count = len(dist)
    if (list_count != dist_count):
        raise Exception('Distances and lists must have the same length!')

    if (interp_count > list_count):
        interp_count = list_count

    weights = []
    for i in range (dist_count):
        if (dist[i] == 0):
            #exact match, no need to interpolate
            interp = my_list[i]
            return interp
        else:
            weight = 1 / dist[i]
            weights.append(weight)

    weight_sum = sum(weights)
    interp = [0] * len(my_list[0])
    for i in range (interp_count):
        interp += [a*b for a,b in zip(weight[i], my_list[i])] / weight_sum
    return interp




def interpolate_prices_and_volume_by_distance(volume_per_list, open_per_list, close_per_list, high_per_list, low_per_list, dist, interp_count):
    interp_volume_per = interpolate_by_distance(volume_per_list, dist, interp_count)
    interp_open_per = interpolate_by_distance(open_per_list, dist, interp_count)
    interp_close_per = interpolate_by_distance(close_per_list, dist, interp_count)
    interp_high_per = interpolate_by_distance(high_per_list, dist, interp_count)
    interp_low_per = interpolate_by_distance(low_per_list, dist, interp_count)
    return (interp_volume_per, interp_open_per, interp_close_per, interp_high_per, interp_low_per)


start_date = datetime(2018, 1, 22, 9, 30)
end_date = datetime(2018, 1, 22, 10, 30)

days_count = 18

symbol = "WEED.TO"
#symbol = "EMHTF"
#symbol = "PRMCF"
#symbol = "ACBFF"
#symbol = "MEDFF"
#symbol = "AMZN"

start, end, dist = prediction.get_closest_distances_time_to_predict_and_distances(symbol, start_date, end_date, days_count)
print start, end, dist

count = len(start)

date_time_per_list = []
volume_per_list = []
open_per_list = []
close_per_list = []
high_per_list = []
low_per_list = []

for i in range (count):
    is_data_available, date_time, volume , opn, close, high, low = read.get_intraday_data(symbol, start[i][0], end[i][0], "1m")
        
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
interp_count = 5

if (interp_count > count):
    interp_count = count

interp_volume_per, interp_open_per, interp_close_per, interp_high_per, interp_low_per = interpolate_prices_and_volume_by_distance(volume_per_list, open_per_list, close_per_list, high_per_list, low_per_list, dist, interp_count)


print interp_close_per
