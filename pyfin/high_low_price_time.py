from read_write import read
from datetime import datetime
from utils import time_op
import matplotlib.pyplot as plt
import numpy as np


start_date = datetime(2017, 12, 28, 9, 30)
end_date = datetime(2017, 12, 28, 15, 59)


is_data_available, date_time, volume , opn, close, high, low = read.get_intraday_data("WEED.TO", start_date, end_date, "1m")

if not (is_data_available):
    exit(0)

high_time = time_op.get_highest_price_time(date_time, high)
print high_time


low_time = time_op.get_lowest_price_time(date_time, low)
print low_time

count = len(close)
range = np.arange(count)
plt.plot(range, close)
plt.show()