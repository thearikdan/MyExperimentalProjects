from datetime import datetime
from utils import time_op
from viz import histogram
from read_write import time_data


N_minute_interval = 1
neighb_point_count = 3
days_count = 30

start_date = datetime(2018, 1, 12, 9, 30)
end_date = datetime(2018, 1, 12, 12, 30)

symbol = "WEED.TO"

max_time_list, min_time_list = time_data.get_high_and_low_price_times(symbol, start_date, end_date, days_count, N_minute_interval, neighb_point_count)

histogram.show_time_hour_minute_histograpm(max_time_list)
histogram.show_time_hour_minute_histograpm(min_time_list)

