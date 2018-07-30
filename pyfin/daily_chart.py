from read_write import read
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from utils import time_op

#start_date = datetime(2018, 1, 5, 9, 30)
#end_date = datetime(2018, 1, 5, 15, 39)

interval = 1
symbol = "0E5M.L"

start_hour, start_min = time_op.get_start_time_for_symbol(symbol)
end_hour, end_min = time_op.get_end_time_for_symbol(symbol)

start_date = datetime(2018, 7, 19, start_hour, start_min)
end_date = datetime(2018, 7, 19, end_hour, end_min)

is_data_available, date_time, volume , opn, close, high, low = read.get_intraday_data("data", symbol, start_date, end_date, interval)

if not (is_data_available):
    exit(0)

plt.plot(date_time, close)
plt.gcf().autofmt_xdate()

plt.show()
