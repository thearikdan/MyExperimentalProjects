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


end_date = datetime(2020, 4, 22, 9, 30)

conn, cur = db.connect_to_database("../../../database/database_settings.txt")

date_list_resorted_list, symbol_list_resorted_list, market_list_resorted_list, percentage_opn_list_resorted_list, opn_nan_ratio_list_resorted_list, current_price_list_resorted_list = db.get_sorted_ascending_trend_by_opening_precentage(conn, cur, filtered_markets, end_date, window_count, window_width, stride, min_price, max_nan_filter)

cur.close()
conn.close()

day_count = len(percentage_opn_list_resorted_list)
for i in range (day_count):
    record_count = len(percentage_opn_list_resorted_list[i])
    for j in range (record_count):
        print("Percentage change " + str(percentage_opn_list_resorted_list[i][j]) + " for company " + symbol_list_resorted_list[i][j] + " on market " + market_list_resorted_list[i][j] + " with nan ratio " + str(opn_nan_ratio_list_resorted_list[i][j]) + " with current price " + str(current_price_list_resorted_list[i][j]))
    print ("---------------------------------------------------------------------------------------------------------")


seconds = time.time() - start_time

mint, s = divmod(seconds, 60)
h, m = divmod(mint, 60)

print ("Elapsed time: %d hours :%02d minutes :%02d seconds" % (h, m, s))
