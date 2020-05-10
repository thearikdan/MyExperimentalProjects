# -*- coding: utf-8 -*-

import sys
sys.path.append("../../..")

from utils.web import download
from utils.db import db

from utils import time_op, constants, sort_op
from datetime import datetime, timedelta
import time
from utils.viz import progress_bar as pb


#target_exchanges = ['nyse', 'nasdaq', 'otcbb']
target_exchanges = ['nyse', 'nasdaq']

max_nan_filter = 0.3
min_price = 70.
min_percentage_up = 1.5
min_volume_filter = 1000000

start_time = time.time()

conn, cursor = db.connect_to_database("../../../database/database_settings.txt")

print ("Retrieving all symbols from database...")
all_symbols, all_exchanges = db.get_all_symbols_and_markets(conn, cursor)

symbols, exchanges = db.filter_by_target_exchanges(all_symbols, all_exchanges, target_exchanges)

count = len(symbols)

available_symbols = []
available_exchanges = []
available_percentages = []

items = list(range(count))
l = len(items)
pb.print_progress(0, l, prefix = 'Progress:', suffix = 'Complete', bar_length = 50)


for i in range(count):

    start_date = datetime(2020, 4, 30, 15, 58)
    end_date = datetime.now() - timedelta(minutes=1)

    symbol = symbols[i]
    is_data_available, date_time, volume, opn, close, high, low = download.get_intraday_data_from_web(symbols[i], start_date, end_date)

    if not is_data_available:
        continue

    count = len(close)

    if close[count - 1] is None:
        continue

    if close[count - 1] < min_price:
        continue


    if close[0] is None:
        continue

    if close[0] == 0:
        continue

    perc = (close[count - 1] - close[0]) * 100 / close[0]
    if perc < min_percentage_up:
        continue

    min_volume = min(volume)
    if min_volume < (min_volume_filter / 1000.0):
        continue

    available_symbols.append(symbols[i])
    available_percentages.append(perc)

    time.sleep(0.1)
    # Update Progress Bar
    pb.print_progress(i + 1, l, prefix = 'Progress:', suffix = 'Complete', bar_length = 50)


cursor.close()
conn.close()


sorted_indices = sort_op.get_sorted_indices(available_percentages)
sorted_symbols = sort_op.get_resorted_list(available_symbols, sorted_indices)
sorted_percentages = sort_op.get_resorted_list(available_percentages, sorted_indices)

count = len(sorted_indices)
for i in range(count):
    print (sorted_symbols[i] + " " + str(sorted_percentages[i]))


seconds = time.time() - start_time

mint, s = divmod(seconds, 60)
h, m = divmod(mint, 60)

print ("--------------------------------------------------------------")
print ("Elapsed time: %d hours :%02d minutes :%02d seconds" % (h, m, s))






