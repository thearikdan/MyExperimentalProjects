from input import read
import time
from datetime import datetime

now = datetime.now()
now_int = int(round(time.mktime(now.timetuple())))
start_date = datetime(2017, 12, 20)
start_date_int = int(round(time.mktime(start_date.timetuple())))


timestamp, volume , open, close, high, low = read.get_intraday_data_from_web("WEED.TO", start_date_int, now_int, "1m")
print open

count = len(timestamp)
for i in range (count):
    date = datetime.fromtimestamp(timestamp[i])
    print date