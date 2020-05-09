import sys
sys.path.append("../..")
from datetime import datetime
from utils.stats import drop_stats


from utils.db import db

symbol = 'TQQQ'
start_date_time = datetime(2020, 5, 4)
end_date_time = datetime(2020, 5, 8)
interval = 1

conn, cur = db.connect_to_database("../../database/database_settings.txt")


is_data_available, dtn, vn, on, cn, hn, ln, c_v, c_o, c_c, c_h, c_l = db.get_etf_intraday_data(symbol, start_date_time, end_date_time, interval)

if not is_data_available:
    print ("No data is available")
    exit(0)

cur.close()
conn.close()

drop_stats = drop_stats.get_drop_stats(cn)
print (drop_stats)