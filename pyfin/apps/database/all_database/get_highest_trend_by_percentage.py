import sys
sys.path.append("../../..")
from datetime import datetime, timedelta
from utils.stats import percentage
from utils.db import db
import time

start_time = time.time()


N = 15

end_date = datetime(2019, 2, 1, 9, 30)
start_date = end_date - timedelta(days = N)

print (start_date)


conn, cur = db.connect_to_database("../../../database/database_settings.txt")

symbols, markets = db.get_all_symbols_and_markets(conn, cur)

count = len (symbols)

symbol_list = []
market_list = []
pecentage_opn_list = []
opn_nan_ratio_list = []

for i in range (count):
    print ("Analysing symbol " + symbols[i] + " on market " + markets[i])
    is_data_available, date, min_volume, max_volume, avg_volume, opn, cls, high, low, volume_nan_ratio, opening_nan_ratio, closing_nan_ratio, high_nan_ratio, low_nan_ratio, _, _, _, _ = db.get_raw_daily_data(conn, cur, markets[i], symbols[i], start_date, end_date)
    if not is_data_available:
        continue
    record_count = len(opn)
    pc = percentage.get_percentage_change_in_one_value(opn[0], opn[record_count-1])
    perc = pc * 100
    nan_ratio = max(opening_nan_ratio[0], opening_nan_ratio[record_count - 1])

    symbol_list.append(symbols[i])
    market_list.append(markets[i])
    pecentage_opn_list.append(perc)
    opn_nan_ratio_list.append(nan_ratio)


print (pecentage_opn_list)

cur.close()
conn.close()

seconds = time.time() - start_time

mint, s = divmod(seconds, 60)
h, m = divmod(mint, 60)

print "Elapsed time: %d hours :%02d minutes :%02d seconds" % (h, m, s)
