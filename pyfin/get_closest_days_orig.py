from read_write import read
from datetime import datetime
import matplotlib.pyplot as plt
from stats import percentage, absolute
from utils import analytics, time_op, sort_op
import numpy as np
import matplotlib.pyplot as plt


start_date = datetime(2018, 1, 19, 9, 30)
end_date = datetime(2018, 1, 19, 10, 30)

days_count = 18

display_count = 5

symbol = "WEED.TO"
#symbol = "EMHTF"
#symbol = "PRMCF"
#symbol = "ACBFF"
#symbol = "MEDFF"


is_data_available, date_time, volume , opn, close, high, low = read.get_intraday_data(symbol, start_date, end_date, "1m")

if not (is_data_available):
    print "No data available"
    exit(0)

date_time_1, volume_per , open_per, close_per, high_per, low_per = percentage.get_percentage_change_in_intraday_prices(date_time, volume , opn, close, high, low)

date_time_per_list, volume_per_list, open_per_list, close_per_list, high_per_list, low_per_list = percentage.get_historical_percentage_data(symbol, start_date, end_date, days_count)

date_time_list, volume_list, open_list, close_list, high_list, low_list = absolute.get_historical_data(symbol, start_date, end_date, days_count)


count = len(close_per_list)

dist_list = []
for i in range (count):
    vec1 = np.array(close_per)
    vec2 = np.array(close_per_list[i])
    dist = analytics.get_distance(vec1, vec2)
    dist_list.append(dist)

print dist_list

sorted_ind = sort_op.get_sorted_indices(dist_list)
print sorted_ind

count = len(sorted_ind)
if count > display_count:
    count = display_count


start_date_str = start_date.strftime("%Y-%m-%d %H:%M")
end_date_str = end_date.strftime("%Y-%m-%d %H:%M")


plt.figure(1)

left  = 0.125  # the left side of the subplots of the figure
right = 0.9    # the right side of the subplots of the figure
bottom = 0.1   # the bottom of the subplots of the figure
top = 0.9      # the top of the subplots of the figure
wspace = 0.2   # the amount of width reserved for space between subplots,
               # expressed as a fraction of the average axis width
hspace = 1.5   # the amount of height reserved for space between subplots,
               # expressed as a fraction of the average axis height

plt.subplots_adjust(left, bottom, right, top,
                wspace, hspace)


title = symbol + ":" + " Percentage changes for " + str(count) + " closest days from " + start_date_str + " to " + end_date_str

plt.suptitle(title, fontsize=12)

for i in range(count):
    ax = plt.subplot(count*100 + 11 + i)
    date_str = (date_time_per_list[sorted_ind[i]][0]).strftime("%Y-%m-%d")
    dist_str = "{:.4f}".format(dist_list[sorted_ind[i]])
    sub_title = "Date: " + date_str + ", distance: " + dist_str
    ax.set_title(sub_title, fontsize=10)
#    plt.tick_params(
#        axis='both',          # changes apply to the x-axis
#        which='both',      # both major and minor ticks are affected
#        bottom='off',      # ticks along the bottom edge are off
#        top='off',         # ticks along the top edge are off
#        labelbottom='off',
#        labelleft='off',
#)
    plt.plot(date_time_per_list[sorted_ind[i]], close_per_list[sorted_ind[i]])
    plt.plot(date_time_per_list[sorted_ind[i]], close_per, 'r')


plt.show()


plt.figure(2)
left  = 0.125  # the left side of the subplots of the figure
right = 0.9    # the right side of the subplots of the figure
bottom = 0.1   # the bottom of the subplots of the figure
top = 0.9      # the top of the subplots of the figure
wspace = 0.2   # the amount of width reserved for space between subplots,
               # expressed as a fraction of the average axis width
hspace = 1.5   # the amount of height reserved for space between subplots,
               # expressed as a fraction of the average axis height

plt.subplots_adjust(left, bottom, right, top,
                wspace, hspace)

title = symbol + ":" + " Price changes for " + str(count) + " closest days from " + start_date_str + " to " + end_date_str

plt.suptitle(title, fontsize=12)

for i in range(count):
    ax = plt.subplot(count*100 + 11 + i)
    date_str = (date_time_per_list[sorted_ind[i]][0]).strftime("%Y-%m-%d")
    dist_str = "{:.4f}".format(dist_list[sorted_ind[i]])
    sub_title = "Date: " + date_str + ", distance: " + dist_str
    ax.set_title(sub_title, fontsize=10)
    plt.plot(date_time, close_list[sorted_ind[i]])
    plt.plot(date_time, close, 'r')


plt.show()


close_list_full = []
for i in range(count):
    start_date_full = date_time_per_list[sorted_ind[i]][0].replace(hour=9, minute=30)
    end_date_full = date_time_per_list[sorted_ind[i]][0].replace(hour=15, minute=59)

    is_data_available_before_full, date_time_before_full, volume_before_full , opn_before_full, close_before_full, high_before_full, low_before_full = read.get_intraday_data(symbol, start_date_full, end_date_full, "1m")
    if not (is_data_available_before_full):
        continue
    close_list_full.append(close_before_full)
#    print date_time_before_full


plt.figure(3)
left  = 0.125  # the left side of the subplots of the figure
right = 0.9    # the right side of the subplots of the figure
bottom = 0.1   # the bottom of the subplots of the figure
top = 0.9      # the top of the subplots of the figure
wspace = 0.2   # the amount of width reserved for space between subplots,
               # expressed as a fraction of the average axis width
hspace = 1.5   # the amount of height reserved for space between subplots,
               # expressed as a fraction of the average axis height

plt.subplots_adjust(left, bottom, right, top,
                wspace, hspace)

title = symbol + ":" + " Full day price changes for " + str(count) + " closest days from " + start_date_str + " to " + end_date_str

plt.suptitle(title, fontsize=12)

for i in range(count):
    ax = plt.subplot(count*100 + 11 + i)
    date_str = (date_time_per_list[sorted_ind[i]][0]).strftime("%Y-%m-%d")
    dist_str = "{:.4f}".format(dist_list[sorted_ind[i]])
    sub_title = "Date: " + date_str + ", distance: " + dist_str
    ax.set_title(sub_title, fontsize=10)
    plt.plot(date_time_before_full, close_list_full[i])
#    plt.plot(date_time, close, 'r')


plt.show()





