import sys
sys.path.append("../..")
from datetime import datetime, timedelta

from utils import analytics
from utils.db import db

market = 'nasdaq'
symbol = 'AMZN'

conn, cur = db.connect_to_database("../../database/database_settings.txt")

all_date_time_list = db.get_all_year_month_day_list_for_symbol(conn, cur, market, symbol)
all_company_ids = db.get_all_company_ids(conn, cur)

for date_time in all_date_time_list:
    for company_id in all_company_ids:
        start_date_time = date_time
        end_date_time = start_date_time + timedelta(days=1)

        is_data_available, dtn, vn, on, cn, hn, ln = db.get_raw_intraday_data_from_company_id(conn, cur, company_id, start_date_time, end_date_time)
        if not is_data_available:
            continue

        min_volume, max_volume, avg_volume, op, cl, high, low, volume_nan_ratio, op_nan_ratio, cl_nan_ratio, high_nan_ratio, low_nan_ratio = analytics.get_daily_data_from_intraday_data( vn, on, cn, hn, ln)
#        print (company_id, date_time, min_volume, max_volume, avg_volume, op, cl, high, low, volume_nan_ratio, op_nan_ratio, cl_nan_ratio, high_nan_ratio, low_nan_ratio)
        db.add_to_daily_prices(conn, cur, company_id, date_time, min_volume, max_volume, avg_volume, op, cl, high, low, volume_nan_ratio, op_nan_ratio, cl_nan_ratio, high_nan_ratio, low_nan_ratio)


cur.close()
conn.close()

