from read_write import read
from datetime import datetime
import matplotlib.pyplot as plt
from stats import percentage
from utils import analytics, time_op, sort_op
import numpy as np
import matplotlib.pyplot as plt


start_date = datetime(2018, 1, 9, 10, 30)
end_date = datetime(2018, 1, 9, 11, 30)

days_count = 18

is_data_available, date_time, volume , opn, close, high, low = read.get_intraday_data("WEED.TO", start_date, end_date, "1m")

if not (is_data_available):
    exit(0)

date_time_1, volume_per , open_per, close_per, high_per, low_per = percentage.get_percentage_change_in_intraday_prices(date_time, volume , opn, close, high, low)
#print close_per

date_time_list = []
close_per_list = []

for i in range (1, days_count):
    new_start_date = time_op.get_date_N_days_ago_from_date(i, start_date)
    new_end_date = time_op.get_date_N_days_ago_from_date(i, end_date)

    is_data_available_before, date_time_before, volume_before , opn_before, close_before, high_before, low_before = read.get_intraday_data("WEED.TO", new_start_date, new_end_date, "1m")
    if not (is_data_available_before):
        continue

    date_time_per_before, volume_per_before , open_per_before, close_per_before, high_per_before, low_per_before = percentage.get_percentage_change_in_intraday_prices(date_time_before, volume_before , opn_before, close_before, high_before, low_before)
    date_time_list.append(date_time_per_before)
    close_per_list.append(close_per_before)


count = len(close_per_list)
dist_list = []
for i in range (count):
    vec1 = np.array(close_per)
    vec2 = np.array(close_per_list[i])
#    print vec2
    dist = analytics.get_distance(vec1, vec2)
    dist_list.append(dist)

print dist_list

sorted_ind = sort_op.get_sorted_indices(dist_list)
print sorted_ind

count = len(sorted_ind)

plt.figure(1)
for i in range(count):
    plt.subplot(count*100 + 11 + i)
    plt.plot(date_time_list[sorted_ind[i]], close_per_list[sorted_ind[i]])

plt.show()


