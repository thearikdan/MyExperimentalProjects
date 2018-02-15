from datetime import datetime, timedelta
from read_write import read
from utils import time_op

def is_intraday_trending(symbol, time_date, minutes_interval, percentage, check_count):
    end_date = time_date
    trending = False
    for i in range (check_count):
        start_date = end_date - timedelta(minutes = minutes_interval)
        is_data_available, date_time, volume , opn, close, high, low = read.get_intraday_data(symbol, start_date, end_date, minutes_interval)
        if not (is_data_available):
            return False
        close_per_change_list = percentage.get_intraday_percentage_change(close)
        if (len (close_per_change_list) != 1):
            return False
        close_per_change = close_per_change_list[0]
        if (percentage > 0):
            if (close_per_change < percentage):
                return False
        elif (percentage < 0):
            if (close_per_change > percentage):
                return False
        end_date = start_date
    return True




