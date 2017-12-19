from input import read
from stats import percentage, absolute
from utils import time, shape, string_op, probability
import numpy as np
from viz import heatmap
from datetime import datetime
import dateutil


symbol = "WEED.TO"
end_date = datetime.today() #today
start_date = end_date + dateutil.relativedelta.relativedelta(months=-3) #month ago

date, num_data = read.get_data_from_web(symbol, start_date, end_date)
sh = np.shape(date)


days = []
for i in range (sh[0]):
    day = time.get_day_number_from_date_string(date[i].strftime("%Y-%m-%d"))
    days.append(day)

#nd = read.get_numeric_data_from_all_data(data)
pc = percentage.get_percentage_change_from_numeric_data(num_data)
perc = pc * 100

mod = 5

shaped_perc = shape.reshape_data(perc, days, mod)

for i in range (mod):
    print shaped_perc[:,i]
    print probability.get_positive_probability_of_day(shaped_perc[:,i])
    print absolute.get_mean_and_deviation_of_day(shaped_perc[:,i])

title = symbol + ": " + start_date.strftime("%Y-%m-%d")+ " to " + end_date.strftime("%Y-%m-%d")


heatmap.show(shaped_perc, title, mod)

