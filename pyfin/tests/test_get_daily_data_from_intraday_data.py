import sys
sys.path.insert(0, "../")

from utils import analytics

vol_list = [100, None, 105, None]
op_list = [None, 2, 1, 3]
cl_list = [6, 4, None, None]
high_list = [7, 5, None, 8]
low_list = [None, None, 1, None]

min_volume, max_volume, avg_volume, op, cl, high, low, volume_none_ratio, op_none_ratio, cl_none_ratio, high_none_ratio, low_none_ratio = analytics.get_daily_data_from_intraday_data(vol_list, op_list, cl_list, high_list, low_list)
print (min_volume, max_volume, avg_volume, op, cl, high, low, volume_none_ratio, op_none_ratio, cl_none_ratio, high_none_ratio, low_none_ratio)

