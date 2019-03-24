import sys
sys.path.append("../..")

#from datetime import datetime
#import matplotlib.pyplot as plt
#from utils.stats import percentage, absolute
#from utils import analytics, time_op, sort_op
from utils.db import db
#import numpy as np


market = "nasdaq"
symbol = "AMZN"

conn, cur = db.connect_to_database("../../database/database_settings.txt")


date_time_list, count_list = db.get_all_days_record_counts(conn, cur, market, symbol)


count = len (date_time_list)
for i in range(count):
    print '%s    %d' % (date_time_list[i].strftime("%Y-%m-%d"), count_list[i])

cur.close()
conn.close()



