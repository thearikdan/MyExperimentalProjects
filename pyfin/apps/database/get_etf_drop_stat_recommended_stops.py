import sys
sys.path.append("../..")
from datetime import datetime
from utils.stats import drop_stats


from utils.db import db

symbol = 'TQQQ'
symbol = 'TNA'
symbol = 'URTY'
symbol = 'SOXL'



start_date_time = datetime(2020, 5, 4)
end_date_time = datetime(2020, 5, 8)
interval = 9

conn, cur = db.connect_to_database("../../database/database_settings.txt")

min_interval = 0
min_percentage = 0

for interval in range (1, 15):
    is_data_available, dtn, vn, on, cn, hn, ln, c_v, c_o, c_c, c_h, c_l = db.get_etf_intraday_data(symbol, start_date_time, end_date_time, interval)

    if not is_data_available:
        print ("No data is available")
        exit(0)


    drop_list, percentages = drop_stats.get_drop_stats(cn)
    if (min(percentages) < min_percentage):
        min_percentage = min(percentages)
        min_interval = interval

#    print (interval)
#    print (len(drop_list))
#    print (min(percentages))
#    print ("\n")

cur.close()
conn.close()


print (min_interval)
print (min_percentage)