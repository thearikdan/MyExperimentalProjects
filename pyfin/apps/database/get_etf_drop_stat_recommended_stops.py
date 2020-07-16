import sys
sys.path.append("../..")
from datetime import datetime
from utils.stats import drop_stats
from utils import time_op

import json
from utils.db import db

symbol = 'TQQQ'
#symbol = 'TNA'
#symbol = 'URTY'
#symbol = 'SOXL'




start_date_time = datetime(2020, 5, 1, 9, 00)
end_date_time = datetime(2020, 7, 16, 00, 00)

data = []

start_hours_minutes = [datetime(2000, 1, 1, 9, 30), datetime(2000, 1, 1, 11, 00), datetime(2000, 1, 1, 12, 00), datetime(2000, 1, 1, 13, 00), datetime(2000, 1, 1, 14, 00), datetime(2000, 1, 1, 15, 00)]
end_hours_minutes = datetime(2000, 1, 1, 16, 00)

time_count = len(start_hours_minutes)

for i in range (time_count):
    print("Analysing start time " + start_hours_minutes[i].strftime("%H:%M:%S"))
    minutes, _ = time_op.get_number_of_minutes_seconds_between_times(start_hours_minutes[i], end_hours_minutes)
    interval_range = range (1, int(minutes / 2))
    print("Number of intervals " + str(int(minutes / 2)))


    min_interval = 0
    min_percentage = 0

    for interval in interval_range:
        is_data_available, dtn, vn, on, cn, hn, ln, c_v, c_o, c_c, c_h, c_l = db.get_etf_intraday_data_after_hours_minutes(symbol, start_date_time, end_date_time, interval, start_hours_minutes[i])


        if not is_data_available:
            print ("No data is available for " + start_hours_minutes[i].strftime("%H:%M:%S"))
            continue

        print ("Analysing interval:" + str(interval))
        drop_list, percentages = drop_stats.get_drop_stats(cn)
        if (min(percentages) < min_percentage):
            min_percentage = min(percentages)
            min_interval = interval

    dict = {"start_time":start_hours_minutes[i].strftime("%H:%M:%S"), "minimum_interval_in_minutes":min_interval, "minimum_percentage": min_percentage, }
    print (dict)
    data.append(dict)


filename = "drop_stats.json"
with open (filename, "w") as f:
    json.dump(data, f)
