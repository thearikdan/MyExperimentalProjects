from input import read
from stats import percentage 
from viz import heatmap
from utils import time, shape, string_op
import numpy as np



name = '/raid/data/pyfin/LEAF.TO.csv'
#name = '/raid/data/pyfin/AMZN.csv'

#name = '/media/ara/HDD/data/Finance/ACB.TO_1_month.csv'
#name = '/media/ara/HDD/data/Finance/WEED.TO_1_month.csv'
#name = '/media/ara/HDD/data/Finance/AMZN_month.csv'


data = read.get_all_data_from_file(name)

date = read.get_date_from_all_data(data)
sh = np.shape(date)

days = []
for i in range (sh[0]):
    day = time.get_day_number_from_date_string(date[i][0])
    days.append(day)

nd = read.get_numeric_data_from_all_data(data)
pc = percentage.get_percentage_change_from_numeric_data(nd)
perc = pc * 100

shaped_perc = shape.reshape_data(perc, days, 5)
#print shaped_perc

comp_name = string_op.get_company_name_from_file_name(name)
title = comp_name + ": " + time.get_date_interval_text(date)

heatmap.show(shaped_perc, title, 5)

