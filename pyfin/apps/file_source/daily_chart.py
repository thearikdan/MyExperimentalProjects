import sys
sys.path.append("../..")

from utils.file_system import read
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from utils import time_op, constants

#start_date = datetime(2018, 1, 5, 9, 30)
#end_date = datetime(2018, 1, 5, 15, 39)

interval = 1
symbol = "AMZN:nasdaq"

start_hour, start_min = time_op.get_start_time_for_symbol(symbol)
end_hour, end_min = time_op.get_end_time_for_symbol(symbol)

start_date = datetime(2019, 01, 30, start_hour, start_min)
end_date = datetime(2019, 02, 04, end_hour, end_min)

is_data_available, date_time, volume , opn, close, high, low = read.get_intraday_data("data", symbol, start_date, end_date, interval, constants.Storage_Type.File_System)

if not (is_data_available):
    exit(0)

plt.plot(date_time, close)
plt.gcf().autofmt_xdate()

plt.show()