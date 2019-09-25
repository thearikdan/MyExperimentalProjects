import sys
sys.path.append("../../..")

from utils.db import db
from utils import time_op, constants, sort_op
from datetime import datetime

interval = 1
YAHOO_PORTFOLIO_EXPORTED_FILE = "quotes.csv"
#target_exchanges = ['nyse', 'nasdaq', 'otcbb']
target_exchanges = ['nyse', 'nasdaq']

max_nan_filter = 0.3
min_price = 10.

conn, cursor = db.connect_to_database("../../../database/database_settings.txt")

symbols, exchanges = db.get_symbols_and_exchanges_from_yahoo_csv(conn, cursor, YAHOO_PORTFOLIO_EXPORTED_FILE, target_exchanges)

count = len(symbols)

available_symbols = []
available_exchanges = []
available_percentages = []

for i in range(count):
    start_hour, start_min = time_op.get_start_time_for_symbol(symbols[i])
    end_hour, end_min = time_op.get_end_time_for_symbol(symbols[i])

    start_date = datetime(2019, 9, 16, start_hour, start_min)
    end_date = datetime(2019, 9, 23, end_hour, end_min)

    symbol = symbols[i]
    perc, cls_start, cls_end, nan_ratio = db.get_interday_percentage_change_by_closing_price(conn, cursor, symbols[i], exchanges[i], start_date, end_date, min_price, max_nan_filter)
    if perc is None:
        continue
    available_symbols.append(symbols[i])
    available_exchanges.append(exchanges[i])
    available_percentages.append(perc)

cursor.close()
conn.close()

sorted_indices = sort_op.get_sorted_indices(available_percentages)
sorted_symbols = sort_op.get_resorted_list(available_symbols, sorted_indices)
sorted_exchanges = sort_op.get_resorted_list(available_exchanges, sorted_indices)
sorted_percentages = sort_op.get_resorted_list(available_percentages, sorted_indices)

count = len(sorted_indices)
for i in range(count):
    print (sorted_symbols[i] + " " + sorted_exchanges[i] + " " + str(sorted_percentages[i]))





