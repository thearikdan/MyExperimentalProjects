import sys
sys.path.append("../../..")

from utils.db import db
from utils import time_op, constants, sort_op
from datetime import datetime
import time
from utils.viz import progress_bar as pb



interval = 1
YAHOO_PORTFOLIO_EXPORTED_FILE = "quotes.csv"
#target_exchanges = ['nyse', 'nasdaq', 'otcbb']
target_exchanges = ['nyse', 'nasdaq']

max_nan_filter = 0.3
min_price = 100.
min_percentage_down = -10.
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
    start_hour, start_min = time_op.get_start_time_for_symbol(symbols[i])
    end_hour, end_min = time_op.get_end_time_for_symbol(symbols[i])

    start_date = datetime(2019, 8, 27, start_hour, start_min)
    end_date = datetime(2019, 9, 27, end_hour, end_min)

    symbol = symbols[i]
    perc, cls_start, cls_end, nan_ratio = db.get_interday_percentage_change_by_closing_price(conn, cursor, symbols[i], exchanges[i], start_date, end_date, min_price, min_volume_filter, max_nan_filter)
    if perc is None:
        continue
    if perc > min_percentage_down:
        continue

    available_symbols.append(symbols[i])
    available_exchanges.append(exchanges[i])
    available_percentages.append(perc)

    time.sleep(0.1)
    # Update Progress Bar
    pb.print_progress(i + 1, l, prefix = 'Progress:', suffix = 'Complete', bar_length = 50)


cursor.close()
conn.close()

sorted_indices = sort_op.get_sorted_indices(available_percentages)
sorted_symbols = sort_op.get_resorted_list(available_symbols, sorted_indices)
sorted_exchanges = sort_op.get_resorted_list(available_exchanges, sorted_indices)
sorted_percentages = sort_op.get_resorted_list(available_percentages, sorted_indices)

count = len(sorted_indices)
for i in range(count):
    print (sorted_symbols[i] + " " + sorted_exchanges[i] + " " + str(sorted_percentages[i]))


seconds = time.time() - start_time

mint, s = divmod(seconds, 60)
h, m = divmod(mint, 60)

print ("--------------------------------------------------------------")
print ("Elapsed time: %d hours :%02d minutes :%02d seconds" % (h, m, s))






