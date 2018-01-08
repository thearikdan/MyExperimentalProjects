from read_write import read
from stats import percentage 
from viz import heatmap
from utils import time_op, shape, string_op
import numpy as np
from datetime import datetime
import dateutil


#name = '/home/ara/Downloads/WEED.TO.csv'

#name = '/media/ara/HDD/data/Finance/ACB.TO_1_month.csv'
#name = '/media/ara/HDD/data/Finance/WEED.TO_1_month.csv'
#name = '/media/ara/HDD/data/Finance/AMZN_month.csv'


#data = read.get_all_data_from_file(name)
#num_data = read.get_numeric_data_from_all_data(data)

#date = read.get_date_from_all_data(data)

symbol = "WEED.TO"
end_date = datetime.today() #today
start_date = end_date + dateutil.relativedelta.relativedelta(months=-1) #month ago

date, num_data = read.get_data_from_web(symbol, start_date, end_date)
sh = np.shape(date)


days = []
for i in range (sh[0]):
    day = time_op.get_day_number_from_date_string(date[i].strftime("%Y-%m-%d"))
    days.append(day)

#nd = read.get_numeric_data_from_all_data(data)
pc = percentage.get_percentage_change_from_numeric_data(num_data)
perc = pc * 100

shaped_perc = shape.reshape_data(perc, days, 5)

#comp_name = string_op.get_company_name_from_file_name(name)
#title = comp_name + ": " + time.get_date_interval_text(date)

title = symbol + ": " + start_date.strftime("%Y-%m-%d")+ " to " + end_date.strftime("%Y-%m-%d")


heatmap.show(shaped_perc, title, 5)

