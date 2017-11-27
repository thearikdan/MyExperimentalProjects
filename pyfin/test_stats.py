from input import read
from stats import percentage 
from viz import colormap
import numpy as np



#name = '/raid/data/pyfin/WEED.TO.csv'
#name = '/media/ara/HDD/data/Finance/WEED.TO.10.22.17.11.22.17.csv'
#name = '/media/ara/HDD/data/Finance/WEED.TO_month.csv'
name = '/media/ara/HDD/data/Finance/AMZN_month.csv'


data = read.get_all_data_from_file(name)

date = read.get_date_from_all_data(data)
nd = read.get_numeric_data_from_all_data(data)

pc = percentage.get_percentage_change_from_numeric_data(nd)
perc = pc * 100

shaped_perc = colormap.reshape_data(perc, 5)

colormap.show(shaped_perc)

