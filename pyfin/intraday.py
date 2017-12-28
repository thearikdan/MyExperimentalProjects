from input import read
import time
from datetime import datetime

#now = datetime.now()
#now_int = int(round(time.mktime(now.timetuple())))
start_date = datetime(2017, 12, 27, 9, 30)
start_date_tuple = start_date.timetuple()
start_date_int = int(time.mktime(start_date_tuple))

end_date = datetime(2017, 12, 27, 16, 00)
end_date_tuple = end_date.timetuple()
end_date_int = int(time.mktime(end_date_tuple))


timestamp, volume , open, close, high, low = read.get_intraday_data_from_web("WEED.TO", start_date_int, end_date_int, "1m")
print open

count = len(timestamp)
for i in range (count):
    date = datetime.fromtimestamp(timestamp[i])
    print date