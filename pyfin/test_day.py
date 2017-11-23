from input import read
from utils import time
import numpy as np

name = '/raid/data/pyfin/WEED.TO.csv'

my_data = read.get_all_data_from_file(name)

date = read.get_date_from_all_data(my_data)
#print date

shape = np.shape(date)
print shape

for i in range (shape[0]):
    print date[i]
    num = time.get_day_number_from_date_string(date[i][0])
    print num
    day = time.get_day_name_from_date_string(date[i][0])
    print day




