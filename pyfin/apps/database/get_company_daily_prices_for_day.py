import sys
sys.path.append("../..")
from datetime import datetime, timedelta

from utils import analytics
from utils.db import db

market = 'nasdaq'
symbol = 'AMZN'
company_id = 139
start_date_time = datetime(2019, 2, 8)
end_date_time = start_date_time + timedelta(days=1)
interval = 1

conn, cur = db.connect_to_database("../../database/database_settings.txt")


is_data_available, dtn, vn, on, cn, hn, ln, c_v, c_o, c_c, c_h, c_l = db.get_intraday_data(conn, cur, market, symbol, start_date_time, end_date_time, interval)

if not is_data_available:
    print ("No data is available")
    exit(0)


print (on)
print (len(on))


min_volume, min_volume_time, max_volume, max_volume_time, avg_volume, opening, closing, high, high_time, low, low_time, volume_none_ratio, opening_nan_ratio, closing_nan_ratio, high_nan_ratio, low_nan_ratio = analytics.get_daily_data_from_intraday_data(dtn, vn, on, cn, hn, ln)
print (min_volume, min_volume_time, max_volume, max_volume_time, avg_volume, opening, closing, high, high_time, low, low_time, volume_none_ratio, opening_nan_ratio, closing_nan_ratio, high_nan_ratio, low_nan_ratio)


is_data_available, dtn, vn, on, cn, hn, ln = db.get_raw_intraday_data_from_company_id(conn, cur, company_id, start_date_time, end_date_time)
if not is_data_available:
    print ("No raw data is available")
    exit(0)

min_volume, min_volume_time, max_volume, max_volume_time, avg_volume, opening, closing, high, high_time, low, low_time, volume_none_ratio, opening_nan_ratio, closing_nan_ratio, high_nan_ratio, low_nan_ratio = analytics.get_daily_data_from_intraday_data(dtn, vn, on, cn, hn, ln)
print (min_volume, min_volume_time, max_volume, max_volume_time, avg_volume, opening, closing, high, high_time, low, low_time, volume_none_ratio, opening_nan_ratio, closing_nan_ratio, high_nan_ratio, low_nan_ratio)


cur.close()
conn.close()

