import dateutil.parser as dparser
import calendar
import numpy as np
from datetime import datetime, timedelta


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
    date_N_days_ago = datetime.now() - timedelta(days=N)
    return date_N_days_ago


def get_date_N_days_ago_from_date(N, date):
    date_N_days_ago = date - timedelta(days=N)
    return date_N_days_ago

