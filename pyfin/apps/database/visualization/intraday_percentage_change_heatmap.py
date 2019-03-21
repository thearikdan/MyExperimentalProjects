import sys
sys.path.append("../../../")

from utils.file_system import read, analysis
from utils.stats import percentage 
from utils.viz import heatmap
from utils import time_op, shape, string_op
#from utils.web import download
from utils.db import db
import numpy as np
from datetime import datetime
import dateutil


conn, cur = db.connect_to_database("../../../database/database_settings.txt")

symbol = "BA"
market = "nyse"

#symbol = "NVDA"
#symbol = "FB"
#symbol = "AMZN"
#market = "nasdaq"

end_date = datetime(2019, 4, 19, 15, 59)
start_date = end_date + dateutil.relativedelta.relativedelta(months=-5) #month ago

#date, num_data = read.get_data_from_web(symbol, start_date, end_date)
is_data_available, date, min_volume, max_volume, avg_volume, opn, cls, high, low, _, _, _, _, _, _, _, _, _ = db.get_raw_daily_data(conn, cur, market, symbol, start_date, end_date)


cur.close()
conn.close()

if not (is_data_available):
    exit(0)

sh = np.shape(date)

days = []
for i in range (sh[0]):
    day = time_op.get_day_number_from_date_string(date[i].strftime("%Y-%m-%d"))
    days.append(day)



#pc = analysis.get_percentage_change_from_numeric_data(num_data)
pc = percentage.get_percentage_change_in_one_value(np.array(opn), np.array(cls))

perc = pc * 100

shaped_perc = shape.reshape_data(perc, days, 5)

#comp_name = string_op.get_company_name_from_file_name(name)
#title = comp_name + ": " + time.get_date_interval_text(date)

title = symbol + ": " + start_date.strftime("%Y-%m-%d")+ " to " + end_date.strftime("%Y-%m-%d")


heatmap.show(shaped_perc, title, 5)

