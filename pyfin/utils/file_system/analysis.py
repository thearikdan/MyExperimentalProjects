from utils.stats import percentage
from utils import time_op, analytics
from utils.file_system import read


def get_percentage_change_from_numeric_data(data):
    op = read.get_opening_price_from_numeric_data(data)
    cp = read.get_closing_price_from_numeric_data(data)
    per = percentage.get_percentage_change(op, cp)
    return per


def get_high_opening_percentage_change_from_numeric_data(data):
    op = read.get_opening_price_from_numeric_data(data)
    hp = read.get_high_price_from_numeric_data(data)
    per = percentage.get_percentage_change(op, hp)
    return per


def get_low_opening_percentage_change_from_numeric_data(data):
    op = read.get_opening_price_from_numeric_data(data)
    lp = read.get_low_price_from_numeric_data(data)
    per = percentage.get_percentage_change(op, lp)
    return per


def get_high_low_percentage_change_from_numeric_data(data):
    hp = read.get_high_price_from_numeric_data(data)
    lp = read.get_low_price_from_numeric_data(data)
    per = percentage.get_percentage_change(lp, hp)
    return per



def get_historical_percentage_data(data_dir, symbol, start_date, end_date, days_count, expected_length):
    date_time_list = []
    volume_per_list = []
    open_per_list = []
    close_per_list = []
    high_per_list = []
    low_per_list = []

    for i in range (1, days_count):
        new_start_date = time_op.get_date_N_days_ago_from_date(i, start_date)
        new_end_date = time_op.get_date_N_days_ago_from_date(i, end_date)

        is_data_available_before, date_time_before, volume_before , opn_before, close_before, high_before, low_before, _, _, _, _, _ = read.get_intraday_data(data_dir, symbol, new_start_date, new_end_date, 1)
        if not (is_data_available_before):
            continue

        date_time_per_before, volume_per_before , open_per_before, close_per_before, high_per_before, low_per_before = percentage.get_percentage_change_in_intraday_prices(date_time_before, volume_before , opn_before, close_before, high_before, low_before)

        count = len(date_time_per_before)
        if (count != expected_length):
            continue

        date_time_list.append(date_time_per_before)
        volume_per_list.append(volume_per_before)
        open_per_list.append(open_per_before)
        close_per_list.append(close_per_before)
        high_per_list.append(high_per_before)
        low_per_list.append(low_per_before)

    return date_time_list, volume_per_list, open_per_list, close_per_list, high_per_list, low_per_list




def get_percentage_change_distance_data(data_dir, symbol, start_date, end_date, days_count):
    is_data_available, date_time, volume , opn, close, high, low, _, _, _, _, _ = read.get_intraday_data(data_dir, symbol, start_date, end_date, 1)

    if not (is_data_available):
        print "No data available"
        return None

    date_time_1, volume_per , open_per, close_per, high_per, low_per = percentage.get_percentage_change_in_intraday_prices(date_time, volume , opn, close, high, low)
    expected_length = len(date_time_1)
    date_time_per_list, volume_per_list, open_per_list, close_per_list, high_per_list, low_per_list = get_historical_percentage_data(data_dir, symbol, start_date, end_date, days_count, 1)

    dist_volume_per_list = analytics.get_distance_list(volume_per, volume_per_list)
    dist_open_per_list = analytics.get_distance_list(open_per, open_per_list)
    dist_close_per_list = analytics.get_distance_list(close_per, close_per_list)
    dist_high_per_list = analytics.get_distance_list(high_per, high_per_list)
    dist_low_per_list = analytics.get_distance_list(low_per, low_per_list)

    return date_time, expected_length, date_time_per_list, \
           (volume, volume_per, volume_per_list, dist_volume_per_list), \
           (opn, open_per, open_per_list, dist_open_per_list), \
           (close, close_per, close_per_list, dist_close_per_list), \
           (high, high_per, high_per_list, dist_high_per_list), \
           (low, low_per, low_per_list, dist_low_per_list)



