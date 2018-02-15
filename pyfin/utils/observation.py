from datetime import datetime, timedelta
from read_write import read
from utils import time_op
from stats import percentage

def is_intraday_trending(symbol, time_date, minutes_interval, perc, check_count):
    end_date = time_date
    check_time = 2 * minutes_interval
    for i in range (check_count):
        start_date = end_date - timedelta(minutes = check_time)
        is_data_available, date_time, volume , opn, close, high, low = read.get_intraday_data(symbol, start_date, end_date, minutes_interval)
        if not (is_data_available):
            return False
        if (perc > 0):
            watch = high
        else:
            watch = low
        watch_per_change_list = percentage.get_intraday_percentage_change(watch)
        if (len (watch_per_change_list) != 1):
            return False
        watch_per_change = watch_per_change_list[0]
        if (perc > 0):
            if (watch_per_change < perc):
                return False
        elif (perc < 0):
            if (watch_per_change > perc):
                return False
        end_date = start_date
    return True




