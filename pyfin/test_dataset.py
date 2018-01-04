from read_write import read
from datetime import datetime
import time

N = 365
now = datetime.now()

from_time = datetime(2000, 1, 1, 10, 00, 00)
to_time = datetime(2000, 1, 1, 11, 30, 00)
#in from_time and to_time only hour, minutes and seconds are important; years and months are ignored


date_time_list, volume_list, open_list, close_list, high_list, low_list = read.get_all_intraday_prices_for_N_days_to_date ("WEED_TO", N, now, from_time, to_time)

print open_list


#29.4082150459 seconds for 1 year


