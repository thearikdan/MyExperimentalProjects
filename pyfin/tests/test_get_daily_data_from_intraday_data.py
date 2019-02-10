import sys
sys.path.insert(0, "../")
import math
from utils import analytics

vol_list = [100., float('nan'), 105., 0.0]
op_list = [float('nan'), 2., 1., 3.]
cl_list = [6., 4., float('nan'), float('nan')]
high_list = [7., 5., float('nan'), 8]
low_list = [float('nan'), 0.0, 1.0, float('nan')]

min_volume, max_volume, avg_volume, op, cl, high, low, volume_none_ratio, op_none_ratio, cl_none_ratio, high_none_ratio, low_none_ratio = analytics.get_daily_data_from_intraday_data(vol_list, op_list, cl_list, high_list, low_list)
print (min_volume, max_volume, avg_volume, op, cl, high, low, volume_none_ratio, op_none_ratio, cl_none_ratio, high_none_ratio, low_none_ratio)

