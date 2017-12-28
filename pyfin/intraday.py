from input import read
from datetime import datetime

start_date = datetime(2017, 12, 27, 9, 30)
end_date = datetime(2017, 12, 27, 16, 00)

date_time, volume , open, close, high, low = read.get_intraday_data_from_web("WEED.TO", start_date, end_date, "1m")

print open
print date_time
