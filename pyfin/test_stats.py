from input import read
from stats import percentage 
from viz import colormap
import numpy as np

name = '/media/ara/HDD/data/Finance/WEED.TO.10.22.17.11.22.17.csv'

data = read.get_all_data_from_file(name)

nd = read.get_numeric_data_from_all_data(data)

pc = percentage.get_percentage_change_from_numeric_data(nd)
perc = pc * 100

#sh = np.shape(perc)
#print sh

perc_shaped = perc.reshape(-1, 5)
print perc_shaped	

colormap.show(perc_shaped)

