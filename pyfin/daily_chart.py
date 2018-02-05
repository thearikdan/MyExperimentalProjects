from read_write import read
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

#start_date = datetime(2018, 1, 5, 9, 30)
#end_date = datetime(2018, 1, 5, 15, 39)

start_date = datetime(2018, 1, 30, 9, 30)
end_date = datetime(2018, 1, 30, 15, 39)

is_data_available, date_time, volume , opn, close, high, low = read.get_intraday_data("AMZN", start_date, end_date, "1m")

if not (is_data_available):
    exit(0)

plt.plot(date_time, close)
plt.gcf().autofmt_xdate()

plt.show()
