import sys
sys.path.append("../..")
from datetime import datetime
from utils.stats import drop_stats
from statistics import mean, stdev
import numpy as np
import pandas as pd
import seaborn as sb
from matplotlib import pyplot as plt
#from scipy import stats


from utils.db import db

symbol = 'TQQQ'
#symbol = 'TNA'
#symbol = 'URTY'
#symbol = 'SOXL'

max_drop_perc = 20

start_date_time = datetime(2020, 5, 1, 9, 00)
end_date_time = datetime(2020, 7, 15, 00, 00)


interval = 190 #get this value from get_etf_drop_stat_recommended_stops.py
#According to get_etf_drop_stat_recommended_stops.py, 190 min is minimal drop with of 17.393%



is_data_available, dtn, vn, on, cn, hn, ln, c_v, c_o, c_c, c_h, c_l = db.get_etf_intraday_data(symbol, start_date_time, end_date_time, interval)
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
df.to_csv("conditional_probabilities.csv")
print (df)




