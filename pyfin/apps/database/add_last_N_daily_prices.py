import sys
sys.path.append("../..")
from datetime import datetime, timedelta
import time
from utils import analytics, time_op
from utils.db import db

from argparse import ArgumentParser


def print_usage():
    print ("Usage: all_last_N_daily_prices.py -n number of days from today")


def get_lat_N_days(N):
    date_times = []
    date_times.append(today)
    for i in range (N):
        day = date.today() - timemedelta(days = i)


parser = ArgumentParser()

parser.add_argument("-n", "--day_count", dest="day_count", help="Specify the number of days from today")


args = parser.parse_args()

params = vars(args)
print (len(sys.argv))

if len(sys.argv) != 3:
    print_usage()
    exit()


start_time = time.time()


N= int(params['day_count'])

date_time_list = time_op.get_last_N_days_list_from_now(N)
print (date_time_list)

conn, cur = db.connect_to_database("../../database/database_settings.txt")

all_company_ids = db.get_all_company_ids(conn, cur)

all_company_ids = [139]

for date_time in date_time_list:
    for company_id in all_company_ids:
        start_date_time = date_time
        end_date_time = start_date_time + timedelta(days=1)

        is_data_available, dtn, vn, on, cn, hn, ln = db.get_raw_intraday_data_from_company_id(company_id, start_date_time, end_date_time)
        if not is_data_available:
            continue

        min_volume, min_volume_times, max_volume, max_volume_times, avg_volume, opening, closing, high, high_times, low, low_times, volume_none_ratio, opening_nan_ratio, closing_nan_ratio, high_nan_ratio, low_nan_ratio = analytics.get_daily_data_from_intraday_data(dtn, vn, on, cn, hn, ln)
#        print (min_volume, min_volume_times, max_volume, max_volume_times, avg_volume, opening, closing, high, high_times, low, low_times, volume_none_ratio, opening_nan_ratio, closing_nan_ratio, high_nan_ratio, low_nan_ratio)
        db.add_to_daily_prices(company_id, date_time, min_volume, min_volume_times, max_volume, max_volume_times, avg_volume, opening, closing, high, high_times, low, low_times, volume_none_ratio, opening_nan_ratio, closing_nan_ratio, high_nan_ratio, low_nan_ratio)


cur.close()
conn.close()

seconds = time.time() - start_time

mint, s = divmod(seconds, 60)
h, m = divmod(mint, 60)

print ("Elapsed time: %d hours :%02d minutes :%02d seconds" % (h, m, s))


