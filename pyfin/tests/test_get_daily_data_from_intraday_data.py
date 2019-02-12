import sys
sys.path.insert(0, "../")
import math
from utils import analytics
from datetime import datetime

time_list = [datetime(2018, 10, 2, 9, 30), datetime(2018, 10, 2, 9, 31), datetime(2018, 10, 2, 9, 32), datetime(2018, 10, 2, 9, 33), datetime(2018, 10, 2, 9, 34)]
vol_list = [100., float('nan'), 105., 0.0, 100.]
op_list = [float('nan'), 2., 1., 3., 5]
cl_list = [6., 4., float('nan'), float('nan'), 5.]
high_list = [7., 5., float('nan'), 8., 8.]
low_list = [float('nan'), 2.0, 1.0, float('nan'), 1.0]

min_volume, min_volume_time, max_volume, max_volume_time, avg_volume, opening, closing, high, high_time, low, low_time, volume_none_ratio, opening_nan_ratio, closing_nan_ratio, high_nan_ratio, low_nan_ratio = analytics.get_daily_data_from_intraday_data(time_list, vol_list, op_list, cl_list, high_list, low_list)
print (min_volume, min_volume_time, max_volume, max_volume_time, avg_volume, opening, closing, high, high_time, low, low_time, volume_none_ratio, opening_nan_ratio, closing_nan_ratio, high_nan_ratio, low_nan_ratio)

