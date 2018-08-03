import sys
sys.path.insert(0, "../")

from read_write import read
from datetime import datetime


start_date = datetime(2018, 2, 6, 9, 30)
end_date = datetime(2018, 2, 6, 15, 39)

is_corrupt = read.is_all_intraday_data_from_file_corrupt("../data/0AH7.L/2018-7-23/1m/0AH7.L_2018-7-23_1m.pickle")
if (is_corrupt):
    print "Test passed"
else:
    print "Test failed"

is_corrupt = read.is_all_intraday_data_from_file_corrupt("../data/AMZN/2018-7-16/1m/AMZN_2018-7-16_1m.pickle")
if (is_corrupt):
    print "Test failed"
else:
    print "Test passed"


