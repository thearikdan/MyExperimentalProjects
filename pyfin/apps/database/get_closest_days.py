import sys
sys.path.append("../..")

from datetime import datetime
import matplotlib.pyplot as plt
from utils.stats import percentage, absolute
from utils import analytics, time_op, sort_op
from utils.db import db, analysis
import numpy as np
from utils.viz import vertical_plots


start_date = datetime(2019, 6, 20, 9, 30)
end_date = datetime(2019, 6, 20, 13, 30)

days_count = 100
interval = 1
display_count = 5


market = "nasdaq"
symbol = "AMZN"


conn, cur = db.connect_to_database("../../database/database_settings.txt")

resorted_date_time_per_list, resorted_dist_close_per_list, resorted_close_per_list, close_per, resorted_date_time_list, resorted_close_list, close = analysis.get_closest_distance_and_info_list_by_closing_price(conn, cur, market, symbol, start_date, end_date, days_count, interval)

count = len(resorted_date_time_per_list)
if count > display_count:
    count = display_count


start_date_str = start_date.strftime("%Y-%m-%d %H:%M")
end_date_str = end_date.strftime("%Y-%m-%d %H:%M")

title = symbol + ":" + " Percentage changes for " + str(count) + " closest days from " + start_date_str + " to " + end_date_str

subtitles = []
for i in range(count):
#    date_str = (date_time_per_list[sorted_ind[i]][0]).strftime("%Y-%m-%d")
#    dist_str = "{:.4f}".format(dist_close_per_list[sorted_ind[i]])
    date_str = (resorted_date_time_per_list[i][0]).strftime("%Y-%m-%d")
    dist_str = "{:.4f}".format(resorted_dist_close_per_list[i])
    subtitle = "Date: " + date_str + ", distance: " + dist_str
    subtitles.append(subtitle)

vertical_plots.show_with_reference(count, start_date, end_date, title, subtitles, resorted_date_time_per_list, resorted_close_per_list, close_per)
vertical_plots.show_with_reference(count, start_date, end_date, title, subtitles, resorted_date_time_list, resorted_close_list, close)



cur.close()
conn.close()

