import sys
sys.path.append("../../..")

from utils.db import db
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from utils import time_op, constants


interval = 1
ONE_DAY_COUNT = 390

market = "nyse"
symbol = "BA"

#market = "nasdaq"
#symbol = "AMZN"


conn, cur = db.connect_to_database("../../../database/database_settings.txt")


start_hour, start_min = time_op.get_start_time_for_symbol(symbol)
end_hour, end_min = time_op.get_end_time_for_symbol(symbol)

start_date = datetime(2019, 03, 01, start_hour, start_min)
end_date = datetime(2019, 03, 15, end_hour, end_min)


is_data_available, date_time, volume , opn, close, high, low, _, _, _, _, _ = db.get_intraday_data(conn, cur, market, symbol, start_date, end_date, interval)


cur.close()
conn.close()


if not (is_data_available):
    exit(0)


date_list = [date.strftime('"%b-%d-%H-%M"') for date in date_time]
count = len(date_list)

date_list_ticks = []
tick_index  = []

for i in range(count):
    if ('9-30' in date_list[i]):
        date_list_ticks.append(date_list[i])
        tick_index.append(i)

print date_list_ticks

xn = range(len(date_list))


plt.plot(xn, volume)
plt.xticks(xn, date_list_ticks)

#plt.plot(date_list, close)
plt.gcf().autofmt_xdate()

plt.show()
