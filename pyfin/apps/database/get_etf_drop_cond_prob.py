import sys
sys.path.append("../..")
from datetime import datetime
from utils.stats import drop_stats
from statistics import mean, stdev
import numpy as np
import pandas as pd
import seaborn as sb
from matplotlib import pyplot as plt
import json
from utils import file_op
from os.path import join


from utils.db import db

OUT_DIR = "data"

symbol = 'TQQQ'
#symbol = 'TNA'
#symbol = 'URTY'
#symbol = 'SOXL'

with open(join(OUT_DIR, symbol + "_" + "drop_stats.json"), "r") as f:
    data = json.load(f)

start_date_time = datetime.strptime(data["start_date_time"], "%m/%d/%Y, %H:%M:%S")
end_date_time = datetime.strptime(data["end_date_time"], "%m/%d/%Y, %H:%M:%S")


intervals_data = data["intervals_data"]

count = len(intervals_data)
file_op.ensure_dir_exists(OUT_DIR)

for i in range (count):
    interval = int(intervals_data[i]["minimum_interval_in_minutes"])
    max_drop_perc = -int(intervals_data[i]["minimum_percentage"]) + 1

    start_hours_minutes_str = intervals_data[i]["start_time"]
    start_hours_minutes = datetime.strptime(start_hours_minutes_str, '%H:%M:%S')


    is_data_available, dtn, vn, on, cn, hn, ln, c_v, c_o, c_c, c_h, c_l = db.get_etf_intraday_data_after_hours_minutes(symbol, start_date_time, end_date_time, interval, start_hours_minutes)
    count = len(cn)
    last_date = dtn[count-1]
    last_price = cn[count-1]

    if not is_data_available:
        print ("No data is available")
        exit(0)


    hist_range = range(-max_drop_perc, 0)
    drop_list, percentages = drop_stats.get_drop_stats(cn)
    hist = np.histogram(percentages, hist_range)

    print(hist)

    count = hist[0].size
    cond_prob = np.empty((count, count))
    cond_prob[:] = np.nan
    for i in range (count):
        h_i = sum(hist[0][:i])
        for j in range (i):
            h_j = sum(hist[0][:j])
            if h_i == 0:
                cond_prob[i][j] = float("nan")
            else:
                cond_prob[i][j] = h_j / h_i

    rows = list(range(-count, 0))
    df = pd.DataFrame(data = cond_prob, index = rows, columns = rows)
    name = symbol + "_" + start_hours_minutes_str + "_conditional_probabilities.csv"
    out_name = join(OUT_DIR, name)
    df.to_csv(out_name)
    print (df)




