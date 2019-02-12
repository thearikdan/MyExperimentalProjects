import dateutil.parser as dparser
import calendar
import numpy as np
import datetime
from datetime import timedelta
import time



def get_int_time(date_time):
    date_time_tuple = date_time.timetuple()
    date_time_int = int(time.mktime(date_time_tuple))
    return date_time_int


def get_date_time_from_timestamp(timestamp):
    date_time = []
    count = len(timestamp)
    for i in range(count):
        dt = datetime.datetime.fromtimestamp(timestamp[i])
        date_time.append(dt)
    return date_time


def get_date_text_from_date_string(date_string):
    date = dparser.parse(date_string)
    return date.strftime('%m/%d/%Y')

def get_day_number_from_date_string(date_string):
    date = dparser.parse(date_string)
    return date.weekday()


def get_day_name_from_date_string(date_string):
    num = get_day_number_from_date_string(date_string)
    return calendar.day_name[num]


def get_date_interval_text(date):
    sh = np.shape(date)

    start_day = get_date_text_from_date_string(date[0][0])
    start_day_name = get_day_name_from_date_string(date[0][0])

    end_day = get_date_text_from_date_string(date[sh[0] - 1][0])
    end_day_name = get_day_name_from_date_string(date[sh[0] - 1][0])

    interval = start_day_name + ", " + start_day + " - " + end_day_name + ", " + end_day
    return interval


def get_date_N_days_ago_from_now(N):
    date_N_days_ago = datetime.datetime.now() - timedelta(days=N)
    return date_N_days_ago


def get_date_N_days_ago_from_date(N, date):
    date_N_days_ago = date - timedelta(days=N)
    return date_N_days_ago


def get_highest_price_time(time, high):
    maximum = max(high)
    index = high.index(maximum)
    return time[index]


def get_lowest_price_time(time, low):
    minimum = min(low)
    index = low.index(minimum)
    return time[index]


def get_date_time_interval_until_end_of_day(my_date_time, reference_end_date_time):
    start_time = my_date_time.replace(hour=reference_end_date_time.hour, minute=reference_end_date_time.minute)
    end_time = my_date_time.replace(hour=15, minute=59)
    return (start_time, end_time)


def get_N_minute_from_one_minute_interval(N, date_time, volume , opn, close, high, low):
    date_time_N = []
    volume_N = []
    open_N = []
    close_N = []
    high_N = []
    low_N = []
    count = len (date_time)
    if (N > count):
        return date_time_N, volume_N , open_N, close_N, high_N, low_N

    new_count = count / N

    for i in range (new_count):
        date_time_N.append(date_time[N * i])
        volume_N.append(volume[N * i])
        open_N.append(opn[N * i])
        close_N.append(close[N * i])
        high_N.append(max(high[N * i : N * (i + 1)]))
        low_N.append(min(low[N * i : N * (i + 1)]))

    return date_time_N, volume_N , open_N, close_N, high_N, low_N


def get_start_time_for_symbol(symbol):
    suffix = ""
    s = symbol.split(".")
    count = len(s)
    if (count != 1):
        suffix = s[count-1]
    start_time = {"" : "9:30",
                 "TO" : "9:30",
                 "V" : "11:00",
                 "L" : "3:00",
                 "AS" : "20:00",
                 "CMX" : "8:20",
                 "SI" : "18:00"}
    if suffix in start_time:
        time = start_time[suffix]
    else:
        time = "9:30"
    hour, minute = time.split(":")
    return int(hour), int(minute)


def get_end_time_for_symbol(symbol):
    suffix = ""
    s = symbol.split(".")
    count = len(s)
    if (count != 1):
        suffix = s[count-1]
    end_time = {"" : "15:59",
                 "TO" : "15:59",
                 "V" : "15:59",
                 "L" : "11:29",
                 "AS" : "1:59",
                 "CMX" : "1:29",
                 "SI" : "23:59"}
    if suffix in end_time:
        time = end_time[suffix]
    else:
        time = "15:39"
    hour, minute = time.split(":")
    return int(hour), int(minute)



def get_date_string_without_padded_zeros(date):
    date_str = date.strftime('%Y-%m-%d').replace("-0", "-")
    return date_str


def get_time_string(date):
    time_str = date.strftime('%H:%M:%S')
#    if time_str[0]=='0':
#        time_str = time_str[1:]
    return time_str


def get_date_time_from_datetime(date_time):
#    date = str(date_time.year) +"-" + str(date_time.month) + "-" + str(date_time.day)
    date = get_date_string_without_padded_zeros(date_time)
#    time = str(date_time.hour) +":" + str(date_time.minute) + ":" + str(date_time.second)
    time = get_time_string(date_time)
    return date, time


def convert_date_to_datetime(dat):
    year, month, day = dat.split("-")
    dt = datetime.datetime(year=int(year), month=int(month), day=int(day))
    return dt



def get_dates_list(records, date_index):
    dates = []
    dates.append(records[0][date_index])

    for item in records:
        count = len(dates)
        if item[date_index] != dates[count - 1]:
            dates.append(item[date_index])
    return dates



def group_intraday_file_records_by_dates(records, date_index):
    dates = get_dates_list(records, date_index)
    dates_count = len(dates)

    grouped_records = []
    for i in range(dates_count):
        grouped_records.append([])

    for item in records:
        for i in range(dates_count):
            if item[date_index] == dates[i]:
                grouped_records[i].append(item)

    return grouped_records



def extract_year_month_day(dt):
    dt_ret = datetime.datetime(year=dt.year, month=dt.month, day=dt.day)
    return dt_ret


def extract_hour_minute_second(dt):
    dt_ret = datetime.time(dt.hour, dt.minute, dt.second)
    return dt_ret


def is_same_day (dt1, dt2):
    dt_ext1 = extract_year_month_day(dt1)
    dt_ext2 = extract_year_month_day(dt2)
    if dt_ext1 == dt.ext2:
        return True
    else:
        return False







