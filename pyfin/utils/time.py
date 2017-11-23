import dateutil.parser as dparser
import calendar


def get_day_number_from_date_string(date_string):
    date = dparser.parse(date_string)
    return date.weekday()


def get_day_name_from_date_string(date_string):
    num = get_day_number_from_date_string(date_string)
    return calendar.day_name[num]



