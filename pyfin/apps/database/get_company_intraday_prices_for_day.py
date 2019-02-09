import sys
sys.path.append("../..")
from datetime import datetime, timedelta


from utils.db import db

market = 'nasdaq'
symbol = 'AMZN'
company_id=139
start_date_time = datetime(2017, 12, 18)
end_date_time = start_date_time + timedelta(days=1)
interval = 1

conn, cur = db.connect_to_database("../../database/database_settings.txt")


is_data_available, dtn, vn, on, cn, hn, ln, c_v, c_o, c_c, c_h, c_l = db.get_intraday_data(conn, cur, market, symbol, start_date_time, end_date_time, interval)

if not is_data_available:
    print ("No data is available")
    exit(0)

print (cn)
print len(cn)

cur.close()
conn.close()



