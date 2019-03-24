import sys
sys.path.append("../../..")
from datetime import datetime, timedelta
from utils.stats import percentage
from utils.db import db
import time
from utils import sort_op

start_time = time.time()


N = 15

end_date = datetime(2019, 3, 22, 9, 30)
start_date = end_date - timedelta(days = N)

print (start_date)


conn, cur = db.connect_to_database("../../../database/database_settings.txt")

symbols, markets = db.get_all_symbols_and_markets(conn, cur)

filtered_markets = ['nasdaq', 'nyse']
max_nan_filter = 0.3

count = len (symbols)

symbol_list = []
market_list = []
percentage_opn_list = []
opn_nan_ratio_list = []

for i in range (count):
    if markets[i] not in filtered_markets:
        continue
    print ("Analysing symbol " + symbols[i] + " on market " + markets[i])
    is_data_available, date, min_volume, max_volume, avg_volume, opn, cls, high, low, volume_nan_ratio, opening_nan_ratio, closing_nan_ratio, high_nan_ratio, low_nan_ratio, _, _, _, _ = db.get_raw_daily_data(conn, cur, markets[i], symbols[i], start_date, end_date)
    if not is_data_available:
        continue
    record_count = len(opn)
    pc = percentage.get_percentage_change_in_one_value(opn[0], opn[record_count-1])
    perc = pc * 100
    nan_ratio = max(opening_nan_ratio[0], opening_nan_ratio[record_count - 1])
    if (nan_ratio > max_nan_filter):
        continue

    symbol_list.append(symbols[i])
    market_list.append(markets[i])
    percentage_opn_list.append(perc)
    opn_nan_ratio_list.append(nan_ratio)



cur.close()
conn.close()


sorted_indices = sort_op.get_sorted_indices(percentage_opn_list)
symbol_list_resorted = sort_op.get_resorted_list(symbol_list, sorted_indices)
market_list_resorted = sort_op.get_resorted_list(market_list, sorted_indices)
percentage_opn_list_resorted = sort_op.get_resorted_list(percentage_opn_list, sorted_indices)
opn_nan_ratio_list_resorted = sort_op.get_resorted_list(opn_nan_ratio_list, sorted_indices)

count = len(percentage_opn_list_resorted)
for i in range (count):
    print("Percentage change " + str(percentage_opn_list_resorted[i]) + " for company " + symbol_list_resorted[i] + " on market " + market_list_resorted[i] + " with nan ratio " + str(opn_nan_ratio_list_resorted[i]))


seconds = time.time() - start_time

mint, s = divmod(seconds, 60)
h, m = divmod(mint, 60)

print "Elapsed time: %d hours :%02d minutes :%02d seconds" % (h, m, s)
