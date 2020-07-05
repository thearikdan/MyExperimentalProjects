import sys
sys.path.append("../..")
from datetime import datetime
from utils.stats import drop_stats
from statistics import mean, stdev
import numpy as np
import pandas as pd
import seaborn as sb
from matplotlib import pyplot as plt


from utils.db import db

symbol = 'TQQQ'
#symbol = 'TNA'
#symbol = 'URTY'
#symbol = 'SOXL'



start_date_time = datetime(2020, 6, 3, 9, 00)
end_date_time = datetime(2020, 7, 3, 00, 00)

interval = 6 #get this value from get_etf_drop_stat_recommended_stops.py


is_data_available, dtn, vn, on, cn, hn, ln, c_v, c_o, c_c, c_h, c_l = db.get_etf_intraday_data(symbol, start_date_time, end_date_time, interval)
count = len(cn)
last_date = dtn[count-1]
last_price = cn[count-1]

if not is_data_available:
    print ("No data is available")
    exit(0)


drop_list, percentages = drop_stats.get_drop_stats(cn)

sb.distplot(percentages, kde=False, rug=True)
plt.show()

