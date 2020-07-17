import sys
sys.path.append("../")
from datetime import datetime

from utils.db import db



symbol = 'TQQQ'

start_date_time = datetime(2020, 7, 14, 9, 00)
end_date_time = datetime(2020, 7, 16, 00, 00)

interval = 5

start_hours_minutes = datetime(2000, 1, 1, 14, 30)


is_data_available, dtn, vn, on, cn, hn, ln, c_v, c_o, c_c, c_h, c_l = db.get_etf_intraday_data_after_hours_minutes(symbol, start_date_time, end_date_time, interval, start_hours_minutes)


if not is_data_available:
    print ("No data is available for " + start_hours_minutes[i].strftime("%H:%M:%S"))

count = len(dtn)
for i in range (count):
    print(dtn[i])
    print (cn[i])
    print("--------------------")
