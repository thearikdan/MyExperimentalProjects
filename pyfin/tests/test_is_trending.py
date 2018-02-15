import sys
sys.path.insert(0, "../")

from utils import observation
from datetime import datetime

symbol = "AMZN"
date_time = datetime(2018, 2, 9, 9, 30)
minutes_interval = 5
#check for average price velocity 0.5% per hour
percentage = 0.005 / 60 * minutes_interval
check_count = 2

trending = observation.is_intraday_trending(symbol, date_time, minutes_interval, percentage, check_count)

if (trending):
    print "Test Failed"
else:
    print "Test Succeeded"


date_time = datetime(2018, 2, 14, 14, 55)
trending = observation.is_intraday_trending(symbol, date_time, minutes_interval, percentage, check_count)

if (trending):
    print "Test Succeeded"
else:
    print "Test Failed"


