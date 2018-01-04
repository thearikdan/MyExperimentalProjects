from read_write import read
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

#start_date = datetime(2018, 1, 3, 9, 30)
#end_date = datetime(2018, 1, 3, 16, 00)

start_date = datetime(2017, 12, 28, 9, 35)
end_date = datetime(2017, 12, 28, 9, 40)

is_data_available, date_time, volume , opn, close, high, low = read.get_intraday_data("WEED.TO", start_date, end_date, "1m")

if not (is_data_available):
    exit(0)

count = len(close)
range = np.arange(count)
plt.plot(range, close)
plt.show()
