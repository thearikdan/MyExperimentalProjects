from read_write import read
from stats import percentage, absolute
from utils import time, shape, string_op, probability
import numpy as np
from viz import heatmap
from datetime import datetime
import dateutil
import pandas as pd


symbol = "WEED.TO"
end_date = datetime.today() #today
start_date = end_date + dateutil.relativedelta.relativedelta(months=-3) #month ago

date, num_data = read.get_data_from_web(symbol, start_date, end_date)
sh = np.shape(date)


days = []
for i in range (sh[0]):
    day = time.get_day_number_from_date_string(date[i].strftime("%Y-%m-%d"))
    days.append(day)

pc = percentage.get_percentage_change_from_numeric_data(num_data)
perc = pc * 100

mod = 5

shaped_perc = shape.reshape_data(perc, days, mod)

data = np.zeros(shape=(3, mod))

for i in range (mod):
    data[0, i] = probability.get_positive_probability_of_day(shaped_perc[:,i])
    data[1, i], data[2, i] = absolute.get_mean_and_deviation_of_day(shaped_perc[:,i])

df = pd.DataFrame(data, columns=['Mon','Tue', 'Wed', 'Thu', 'Fri'], index=['Probability of positive','Mean','Deviation'])
print df

