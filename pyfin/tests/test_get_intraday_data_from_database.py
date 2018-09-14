import sys
sys.path.insert(0, "../")

from utils import db

conn, cur = db.connect_to_database("../database/database_settings.txt")


is_data_available, date_time, volume , opn, close, high, low = db.get_intraday_data(conn, cur, "nasdaq", "AMZN", "2018-5-2", "2018-5-3", 1)

cur.close()
conn.close()
