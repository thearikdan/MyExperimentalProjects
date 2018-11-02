from read_write import read
from datetime import datetime
import matplotlib.pyplot as plt
from stats import percentage

start_date = datetime(2017, 12, 28, 10, 30)
end_date = datetime(2017, 12, 28, 11, 30)

is_data_available, date_time, volume , opn, close, high, low = read.get_intraday_data("WEED.TO", start_date, end_date, "1m")

if not (is_data_available):
    exit(0)

date_time_1, volume_per , open_per, close_per, high_per, low_per = percentage.get_percentage_change_in_intraday_prices(date_time, volume , opn, close, high, low)
print close_per
