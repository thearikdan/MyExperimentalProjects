import sys
sys.path.append("../..")


from utils.file_system import read
from utils.stats import percentage 
from utils.viz import colormap
from utils import time_op, shape
import numpy as np



#name = '/raid/data/pyfin/LEAF.TO.csv'
#name = '/raid/data/pyfin/AMZN.csv'

#name = '/media/ara/HDD/data/Finance/ACB.TO.csv'
name = '/media/ara/HDD/data/Finance/WEED.TO_1_month.csv'
#name = '/media/ara/HDD/data/Finance/AMZN_month.csv'


data = read.get_all_data_from_file(name)

date = read.get_date_from_all_data(data)
sh = np.shape(date)

days = []
for i in range (sh[0]):
    day = time_op.get_day_number_from_date_string(date[i][0])
    days.append(day)

nd = read.get_numeric_data_from_all_data(data)
pc = percentage.get_percentage_change_from_numeric_data(nd)
perc = pc * 100

shaped_perc = shape.reshape_data(perc, days, 5)
#print shaped_perc

colormap.show(shaped_perc, 5)

