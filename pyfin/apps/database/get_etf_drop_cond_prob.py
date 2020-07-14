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

max_drop_perc = 10

start_date_time = datetime(2020, 7, 1, 9, 00)
end_date_time = datetime(2020, 7, 14, 00, 00)


interval = 13 #get this value from get_etf_drop_stat_recommended_stops.py


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

count = hist[0].size
cond_prob = np.empty((count, count))
cond_prob[:] = np.nan
for i in range (count):
    h_i = hist[0][i]
    for j in range (i, count):
        h_j = hist[0][j]
        if h_j == 0:
            cond_prob[i][j] = float("nan")
        else:
            cond_prob[i][j] = h_i / h_j

rows = list(range(-count, 0))
df = pd.DataFrame(data = cond_prob, index = rows, columns = rows)
print (df)




