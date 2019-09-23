import sys
sys.path.append("../../..")

from utils.db import db
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from utils import time_op, constants


def get_sparse_date_list(date_list, tick_count):
    sparse_list = []
    sparse_index_list = []
    count = len(date_list)
    inter = int((count - 2) / (tick_count - 1))
    sparse_list.append(date_list[0])
    sparse_index_list.append(0)
    for i in range(tick_count - 2):
        sparse_list.append(date_list[(i + 1) * inter])
        sparse_index_list.append((i + 1) * inter)
    sparse_list.append(date_list[count - 1])
    sparse_index_list.append(count-1)
    return sparse_list, sparse_index_list


interval = 1
market = "nyse"
symbol = "BA"

market = "nasdaq"
symbol = "NVDA"


conn, cur = db.connect_to_database("../../../database/database_settings.txt")


start_hour, start_min = time_op.get_start_time_for_symbol(symbol)
end_hour, end_min = time_op.get_end_time_for_symbol(symbol)

start_date = datetime(2019, 8, 23, start_hour, start_min)
end_date = datetime(2019, 9, 23, end_hour, end_min)


is_data_available, date_time, volume , opn, close, high, low, _, _, _, _, _ = db.get_intraday_data(conn, cur, market, symbol, start_date, end_date, interval)


cur.close()
conn.close()


if not (is_data_available):
    exit(0)


date_list = [date.strftime('"%d-%m-%y"') for date in date_time]

bins = 5
sparse_date_list, sparse_index_list = get_sparse_date_list(date_list, bins)
xn = range(len(date_list))


plt.plot(xn, close)
plt.xticks(sparse_index_list, sparse_date_list)
plt.locator_params(axis='x', nbins=bins)


plt.gcf().autofmt_xdate()

plt.show()


