import sys
sys.path.append("../..")

from utils.db import db
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from utils import time_op, constants

#start_date = datetime(2018, 1, 5, 9, 30)
#end_date = datetime(2018, 1, 5, 15, 39)

interval = 1
market = "nyse"
symbol = "BA"


conn, cur = db.connect_to_database("../../database/database_settings.txt")


start_hour, start_min = time_op.get_start_time_for_symbol(symbol)
end_hour, end_min = time_op.get_end_time_for_symbol(symbol)

start_date = datetime(2019, 02, 25, start_hour, start_min)
end_date = datetime(2019, 02, 28, end_hour, end_min)


is_data_available, date_time, volume , opn, close, high, low, _, _, _, _, _ = db.get_intraday_data(conn, cur, market, symbol, start_date, end_date, interval)


cur.close()
conn.close()


if not (is_data_available):
    exit(0)

plt.plot(date_time, close)
plt.gcf().autofmt_xdate()

plt.show()
