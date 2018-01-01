from read_write import read
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

start_date = datetime(2017, 12, 28, 9, 30)
end_date = datetime(2017, 12, 28, 16, 00)

#is_data_available, date_time, volume , opn, close, high, low = read.get_intraday_data_from_web("WEED.TO", start_date, end_date, "1m")
is_data_available, date_time, volume , opn, close, high, low = read.get_intraday_data("WEED.TO", start_date, end_date, "1m")

if not (is_data_available):
    exit(0)

high_price = max(close)
print high_price

ind = close.index(high_price)
print ind

max_time = date_time[ind]
print max_time

count = len(close)
range = np.arange(count)
plt.bar(range, close)
plt.show()
