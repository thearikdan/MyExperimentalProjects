import sys
sys.path.append("../../..")
from datetime import datetime
from utils.db import db
import time




start_time = time.time()


N = 15
filtered_markets = ['nasdaq', 'nyse']
#filtered_markets = ['tsx']
max_nan_filter = 0.3
min_price = 8.
window_count = 5
window_width = 7
stride = 3


end_date = datetime(2019, 4, 19, 9, 30)

conn, cur = db.connect_to_database("../../../database/database_settings.txt")

symbol_list_resorted, market_list_resorted, percentage_opn_list_resorted, opn_nan_ratio_list_resorted, current_price_list_resorted = db.get_sorted_ascending_trend_by_opening_precentage(conn, cur, filtered_markets, end_date, window_count, window_width, stride, min_price, max_nan_filter)

cur.close()
conn.close()

count = len(percentage_opn_list_resorted)
for i in range (count):
    print("Percentage change " + str(percentage_opn_list_resorted[i]) + " for company " + symbol_list_resorted[i] + " on market " + market_list_resorted[i] + " with nan ratio " + str(opn_nan_ratio_list_resorted[i]) + " with current price " + str(current_price_list_resorted[i]))


seconds = time.time() - start_time

mint, s = divmod(seconds, 60)
h, m = divmod(mint, 60)

print "Elapsed time: %d hours :%02d minutes :%02d seconds" % (h, m, s)
