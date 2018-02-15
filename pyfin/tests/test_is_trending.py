import sys
sys.path.insert(0, "../")

from utils import observation
from datetime import datetime

symbol = "AMZN"
date_time = datetime(2018, 2, 9, 9, 30)
minutes_interval = 5
percentage = 0.001
check_count = 2

trending = observation.is_intraday_trending(symbol, date_time, minutes_interval, percentage, check_count)

if (trending):
    print "Test Failed"
else:
    print "Test Succeeded"


date_time = datetime(2018, 2, 9, 12, 30)
trending = observation.is_intraday_trending(symbol, date_time, minutes_interval, percentage, check_count)

if (trending):
    print "Test Succeeded"
else:
    print "Test Failed"


