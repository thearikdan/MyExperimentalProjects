from datetime import datetime, timedelta
from utils import prediction, analytics
from read_write import read
from utils import file_op, sort_op
from os import path

#import matplotlib.pyplot as plt


start_date = datetime(2018, 1, 24, 9, 30)
end_date = datetime(2018, 1, 24, 10, 30)

real_start_date = end_date + timedelta(minutes = 1)
real_end_date = end_date.replace(hour=15, minute=59)

DAYS_TO_ANALYSE = 30


#symbol = "WEED.TO"
#symbol = "EMHTF"
#symbol = "PRMCF"
#symbol = "ACBFF"
#symbol = "MEDFF"
symbol = "AMZN"

ROOT_DIR = "results/analysis"
DIR_NAME = path.join(ROOT_DIR, symbol)
file_op.ensure_dir_exists(DIR_NAME)


days_count_list = []
interp_count_list = []
distance_list = []

is_data_available, date_time_real, volume_real, opn_real, close_real, high_real, low_real = read.get_intraday_data(symbol, real_start_date, real_end_date, "1m")

if not (is_data_available):
    print "No real data available"
    exit(0)

for i in range (2, DAYS_TO_ANALYSE):
    for j in range (1, i):
        predicted_prices, times, closest_date_times, distances = prediction.get_linear_interpolation_prediction(symbol, start_date, end_date, i, j)
        distance = analytics.get_distance(close_real, predicted_prices)
        
        days_count_list.append(i)
        interp_count_list.append(j)
        distance_list.append(distance)
        
        info = "Analysed days: %d, Interpolated Closest Days: %d, distance %f\n" % (i, j, distance)
        print info


sorted_ind = sort_op.get_sorted_indices(distance_list)


title = "LinearInterpolationPrediction_%s_to_%s.txt" % (start_date.strftime("%Y-%m-%d-%H:%M"), end_date.strftime("%Y-%m-%d-%H:%M"))
filename = path.join(DIR_NAME, title) 
f = open(filename, 'w')
title_str = "Linear Interpolation Prediction for %s from %s to %s\n\n" % (symbol, start_date.strftime("%Y-%m-%d-%H:%M"), end_date.strftime("%Y-%m-%d-%H:%M"))
f.write(title_str)

count = len(sorted_ind)
for i in range (count):
    info = "Analysed days: %d, Interpolated Closest Days: %d, distance %f\n" % (days_count_list[sorted_ind[i]], interp_count_list[sorted_ind[i]], distance_list[sorted_ind[i]])
    f.write(info)



f.close

#print predicted_prices
#print times
#print closest_date_times
#print distances

#plt.plot(times, predicted_prices)
#plt.gcf().autofmt_xdate()

#plt.show()


