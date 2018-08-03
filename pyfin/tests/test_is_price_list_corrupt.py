import sys
sys.path.insert(0, "../")

from read_write import read
from datetime import datetime


date_time, volume , opn, close, high, low = read.get_all_intraday_data_from_file("../data/0AH7.L/2018-7-23/1m/0AH7.L_2018-7-23_1m.pickle")
is_corrupt = read.is_price_list_corrupt(close)
if (is_corrupt):
    print "Test passed"
else:
    print "Test failed"


date_time, volume , opn, close, high, low = read.get_all_intraday_data_from_file("../data/AMZN/2018-7-16/1m/AMZN_2018-7-16_1m.pickle")
is_corrupt = read.is_price_list_corrupt(close)
if (is_corrupt):
    print "Test failed"
else:
    print "Test passed"


