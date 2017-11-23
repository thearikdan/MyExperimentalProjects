from input import read
from stats import percentage 
from viz import colormap
import numpy as np

name = '/raid/data/pyfin/WEED.TO.csv'

data = read.get_all_data_from_file(name)

date = read.get_date_from_all_data(my_data)
nd = read.get_numeric_data_from_all_data(data)

pc = percentage.get_percentage_change_from_numeric_data(nd)
perc = pc * 100

#sh = np.shape(perc)
#print sh

perc_shaped = perc.reshape(-1, 5)
print perc_shaped	

colormap.show(date, perc_shaped)

