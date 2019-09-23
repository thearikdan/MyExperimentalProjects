import sys
sys.path.append("../../..")
from datetime import datetime
from utils.db import db
import time




start_time = time.time()


day_count = 3
filtered_markets = ['nasdaq', 'nyse']
#filtered_markets = ['tsx']
max_nan_filter = 0.3
min_price = 80.
min_percentage = 6

end_date = datetime(2019, 8, 14, 00, 00, 00)

conn, cur = db.connect_to_database("../../../database/database_settings.txt")

all_date_list = db.get_all_year_month_day_list_for_symbol(conn, cur, "nasdaq", "AMZN")

end_date_index = all_date_list.index(end_date)

date_list = all_date_list[end_date_index - day_count + 1: end_date_index + 1]
start_date = date_list[0]

symbols, markets = db.get_all_symbols_and_markets(conn, cur)

selected_symbols = []
selected_markets = []
selected_percentages = []
nan_ratios = []
start_prices = []
end_prices = []

symbol_count = len(symbols)
for i in range (symbol_count):
    if markets[i] not in filtered_markets:
        continue
    print("Analysing symbol " + symbols[i] + " on market " + markets[i])
    percentage, start_price, end_price, nan_ratio = db.get_interday_percentage_change_by_closing_price(conn, cur, symbols[i], markets[i], start_date, end_date, min_price, max_nan_filter)
    if (percentage >= min_percentage):
        selected_symbols.append(symbols[i])
        selected_markets.append(markets[i])
        selected_percentages.append(percentage)
        start_prices.append(start_price)
        end_prices.append(end_price)
        nan_ratios.append(nan_ratio)

record_count = len(selected_symbols)
for i in range (record_count):
    print("Percentage change " + str(selected_percentages[i]) + " for company " + selected_symbols[i] + " on market " + selected_markets[i] + " with nan ratio " + str(nan_ratios[i]) + " with start price " + str(start_prices[i]) + " with end price " + str(end_prices[i]))
    print ("---------------------------------------------------------------------------------------------------------")

cur.close()
conn.close()

seconds = time.time() - start_time

mint, s = divmod(seconds, 60)
h, m = divmod(mint, 60)

print "Elapsed time: %d hours :%02d minutes :%02d seconds" % (h, m, s)
