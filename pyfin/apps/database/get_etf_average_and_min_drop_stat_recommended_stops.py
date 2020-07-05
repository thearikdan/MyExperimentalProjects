import sys
sys.path.append("../..")
from datetime import datetime
from utils.stats import drop_stats
from statistics import mean, stdev


from utils.db import db

symbol = 'TQQQ'
#symbol = 'TNA'
#symbol = 'URTY'
#symbol = 'SOXL'



start_date_time = datetime(2020, 6, 3, 9, 00)
end_date_time = datetime(2020, 7, 3, 00, 00)

interval = 6 #get this value from get_etf_drop_stat_recommended_stops.py


is_data_available, dtn, vn, on, cn, hn, ln, c_v, c_o, c_c, c_h, c_l = db.get_etf_intraday_data(symbol, start_date_time, end_date_time, interval)
count = len(cn)
last_date = dtn[count-1]
last_price = cn[count-1]

if not is_data_available:
    print ("No data is available")
    exit(0)


drop_list, percentages = drop_stats.get_drop_stats(cn)
avg_percentage = mean(percentages)
sigma = stdev(percentages)
min_percentage = min(percentages)

print(last_date)
print ("Last price: " + str(last_price) + "\n")
print ("Average drop percentage: " + str(avg_percentage))
print ("Stop price for average drop percentage: " + str(last_price * (1 + avg_percentage/100.)) + "\n") #+ because avg_percentage is negative

print ("68.27% of drop percentage (mean - sigma): " + str(avg_percentage - sigma))
print ("Stop price for 68.27% of drop percentage (mean - sigma): " + str(last_price * (1 + (avg_percentage - sigma)/100.)) + "\n") #+ because avg_percentage is negative

print ("95.45% of drop percentage (mean - 2 * sigma): " + str(avg_percentage - 2 * sigma))
print ("Stop price for 95.45% of drop percentage (mean - 2 * sigma): " + str(last_price * (1 + (avg_percentage -2 * sigma)/100.)) + "\n") #+ because avg_percentage is negative

print ("99.73% of drop percentage (mean - 3 * sigma): " + str(avg_percentage - 3 * sigma))
print ("Stop price for 99.73% of drop percentage (mean - 3 * sigma): " + str(last_price * (1 + (avg_percentage -3 * sigma)/100.)) + "\n") #+ because avg_percentage is negative

print ("Minimum drop percentage: " + str(min_percentage))
print ("Stop price for minimum drop percentage: " + str(last_price * (1 + min_percentage/100.)) + "\n") #+ because min_percentage is negative
