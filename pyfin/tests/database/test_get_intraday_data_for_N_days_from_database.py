import sys
sys.path.insert(0, "../..")

from datetime import datetime

from utils import db

conn, cur = db.connect_to_database("../../database/database_settings.txt")


date_time1 = datetime(2018, 5, 2, 9, 30)
date_time2 = datetime(2018, 5, 3, 9, 32)

days_count = 20

data_list = db.get_intraday_data_for_N_days(conn, cur, "nasdaq", "AMZN", days_count, date_time1, date_time2, 1)
print data_list

print len(data_list)

cur.close()
conn.close()
