import sys
sys.path.insert(0, "../..")

from datetime import datetime, timedelta

from utils import db

conn, cur = db.connect_to_database("../../database/database_settings.txt")

date_time1 = datetime(2018, 5, 3, 9, 30)
date_time2 = datetime(2018, 5, 3, 9, 32)

is_data_available, date_time, volume , opn, cls, high, low, c_v, c_o, c_c, c_h, c_l = db.get_intraday_data(conn, cur, "nasdaq", "AMZN", date_time1, date_time2, 1)

print cls



date_time3 = datetime(2018, 5, 2, 9, 30)
date_time4 = datetime(2018, 5, 2, 9, 32)

is_data_available, date_time, volume , opn, cls, high, low, c_v, c_o, c_c, c_h, c_l = db.get_intraday_data(conn, cur, "nasdaq", "AMZN", date_time3, date_time4, 1)

print cls


date_time5 = date_time1 - timedelta(days=1)
date_time6 = date_time2 - timedelta(days=1)


is_data_available, date_time, volume , opn, cls, high, low, c_v, c_o, c_c, c_h, c_l = db.get_intraday_data(conn, cur, "nasdaq", "AMZN", date_time5, date_time6, 1)

print cls

cur.close()
conn.close()
