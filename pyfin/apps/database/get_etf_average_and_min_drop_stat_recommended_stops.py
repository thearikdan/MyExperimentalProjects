import sys
sys.path.append("../..")
from datetime import datetime
from utils.stats import drop_stats
from statistics import mean 


from utils.db import db

#symbol = 'TQQQ'
symbol = 'TNA'
#symbol = 'URTY'
#symbol = 'SOXL'



start_date_time = datetime(2020, 4, 28)
end_date_time = datetime(2020, 5, 27)

interval = 8 #get this value from get_etf_drop_stat_recommended_stops.py

conn, cur = db.connect_to_database("../../database/database_settings.txt")


is_data_available, dtn, vn, on, cn, hn, ln, c_v, c_o, c_c, c_h, c_l = db.get_etf_intraday_data(symbol, start_date_time, end_date_time, interval)

if not is_data_available:
    print ("No data is available")
    exit(0)


drop_list, percentages = drop_stats.get_drop_stats(cn)
avg_percentage = mean(percentages)
min_percentage = min(percentages)


cur.close()
conn.close()

print (avg_percentage)
print (min_percentage)
