import sys
sys.path.append("..")

from utils.web import download
from datetime import datetime, timedelta


start_date = datetime.now() - timedelta(minutes=2)
end_date = datetime.now()

symbol = "TQQQ"
is_data_available, date_time, volume, opn, close, high, low = download.get_intraday_data_from_web(symbol, start_date, end_date)

print (close)
