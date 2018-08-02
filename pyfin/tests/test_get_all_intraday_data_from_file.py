import sys
sys.path.insert(0, "../")

from read_write import read
from datetime import datetime


start_date = datetime(2018, 2, 6, 9, 30)
end_date = datetime(2018, 2, 6, 15, 39)

#date_time, volume , opn, close, high, low = read.get_all_intraday_data_from_file("../data/0AH7.L/2018-7-23/1m/0AH7.L_2018-7-23_1m.pickle")
date_time, volume , opn, close, high, low = read.get_all_intraday_data_from_file("../data/AMZN/2018-7-16/1m/AMZN_2018-7-16_1m.pickle")


print date_time
print volume
print opn
print close
print high
print low
