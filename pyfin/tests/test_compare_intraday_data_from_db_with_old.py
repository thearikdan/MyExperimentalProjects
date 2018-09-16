import sys
sys.path.insert(0, "../")

from read_write import read
from datetime import datetime
from utils import db


epsilon = 0.001

start_date = datetime(2018, 5, 2, 9, 30)
end_date = datetime(2018, 5, 2, 15, 59)

is_data_available, date_time, volume , opn, close, high, low = read.get_intraday_data("/media/hddx/datasets/pyfin/data_v1", "AMZN", start_date, end_date, 1)

print date_time

conn, cur = db.connect_to_database("../database/database_settings.txt")

is_data_available_db, date_time_db, volume_db, opn_db, close_db, high_db, low_db = db.get_intraday_data(conn, cur, "nasdaq", "AMZN", "2018-5-2", "2018-5-3", 1)

print date_time_db

cur.close()
conn.close()

count = min(len(close_db), len(close))

for i in range(count):
    if abs(float(close_db[i]) - close[i]) > epsilon:
        print "Test failed"
        break

print "Test succeeded"
