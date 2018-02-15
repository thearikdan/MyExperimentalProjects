from utils import observation
from datetime import datetime

symbol = "AMZN"
date_time = datetime(2018, 1, 12, 9, 30)
minutes_interval = 5
percentage = 0.001
check_count = 2

trending = is_intraday_trending(symbol, time_date, minutes_interval, percentage, check_count)


