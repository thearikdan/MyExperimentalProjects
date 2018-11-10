import sys
sys.path.append("../..")

from datetime import datetime
import matplotlib.pyplot as plt
from utils.stats import percentage, absolute
from utils import analytics, time_op, sort_op
from utils.db import db, analysis
import numpy as np
from utils.viz import vertical_plots


start_date = datetime(2018, 10, 2, 9, 30)
end_date = datetime(2018, 10, 2, 13, 30)

days_count = 100

display_count = 5


market = "nasdaq"
symbol = "AMZN"


conn, cur = db.connect_to_database("../../database/database_settings.txt")


date_time, expected_length, date_time_per_list, _, _, (close, close_per, close_per_list, dist_close_per_list), _, _ = analysis.get_percentage_change_distance_data(conn, cur, market, symbol, start_date, end_date, days_count)


date_time_list, volume_list, open_list, close_list, high_list, low_list, _, _, _, _, _ = db.get_historical_intraday_data_for_N_days(conn, cur, market, symbol, start_date, end_date, days_count, 1, expected_length + 1)


sorted_ind = sort_op.get_sorted_indices(dist_close_per_list)

count = len(sorted_ind)
if count > display_count:
    count = display_count


resorted_date_time_per_list = sort_op.get_resorted_list(date_time_per_list, sorted_ind)
resorted_close_per_list = sort_op.get_resorted_list(close_per_list, sorted_ind)

start_date_str = start_date.strftime("%Y-%m-%d %H:%M")
end_date_str = end_date.strftime("%Y-%m-%d %H:%M")

title = symbol + ":" + " Percentage changes for " + str(count) + " closest days from " + start_date_str + " to " + end_date_str

subtitles = []
for i in range(count):
    date_str = (date_time_per_list[sorted_ind[i]][0]).strftime("%Y-%m-%d")
    dist_str = "{:.4f}".format(dist_close_per_list[sorted_ind[i]])
    subtitle = "Date: " + date_str + ", distance: " + dist_str
    subtitles.append(subtitle)

vertical_plots.show_with_reference(count, start_date, end_date, title, subtitles, resorted_date_time_per_list, resorted_close_per_list, close_per)



resorted_close_list = sort_op.get_resorted_list(close_list, sorted_ind)
date_time_list = []

title = symbol + ":" + " Price changes for " + str(count) + " closest days from " + start_date_str + " to " + end_date_str
subtitles = []
for i in range(count):
    date_str = (date_time_per_list[sorted_ind[i]][0]).strftime("%Y-%m-%d")
    dist_str = "{:.4f}".format(dist_close_per_list[sorted_ind[i]])
    subtitle = "Date: " + date_str + ", distance: " + dist_str
    subtitles.append(subtitle)
    date_time_list.append(date_time)

vertical_plots.show_with_reference(count, start_date, end_date, title, subtitles, date_time_list, resorted_close_list, close)



full_count = len(sorted_ind)
close_list_full = []
date_time_full_list = []

for i in range(full_count):
    start_date_full = date_time_per_list[sorted_ind[i]][0].replace(hour=9, minute=30)
    end_date_full = date_time_per_list[sorted_ind[i]][0].replace(hour=15, minute=59)

    is_data_available_before_full, date_time_before_full, volume_before_full , opn_before_full, close_before_full, high_before_full, low_before_full, _, _, _, _, _ = db.get_intraday_data(conn, cur, market, symbol, start_date_full, end_date_full, 1)
    if not (is_data_available_before_full):
        continue
    close_list_full.append(close_before_full)
    date_time_full_list.append(date_time_before_full)


if (count > full_count):
    count = full_count

start_date_full_str = start_date_full.strftime("%Y-%m-%d %H:%M")
end_date_full_str = end_date_full.strftime("%Y-%m-%d %H:%M")

title = symbol + ":" + " Full day price changes for " + str(count) + " closest days from " + start_date_full_str + " to " + end_date_full_str

subtitles = []
for i in range(count):
    date_str = (date_time_full_list[i][0]).strftime("%Y-%m-%d")
    dist_str = "{:.4f}".format(dist_close_per_list[sorted_ind[i]])
    subtitle = "Date: " + date_str + ", distance: " + dist_str
    subtitles.append(subtitle)

vertical_plots.show(count, start_date_full, end_date_full, title, subtitles, date_time_full_list, close_list_full)


cur.close()
conn.close()

