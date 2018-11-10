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


#date_time_list, length_list = db.get_all_days_record_counts(conn, cur, market, symbol)
date_time_list = db.get_all_days_record_counts(conn, cur, market, symbol)

print date_time_list
#print len_list

cur.close()
conn.close()



