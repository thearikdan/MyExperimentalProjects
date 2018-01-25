from datetime import datetime, timedelta
from utils import prediction, analytics
from read_write import read

#import matplotlib.pyplot as plt


start_date = datetime(2018, 1, 24, 9, 30)
end_date = datetime(2018, 1, 24, 10, 30)

real_start_date = end_date + timedelta(minutes = 1)
real_end_date = end_date.replace(hour=15, minute=59)

days_count = 30

interp_count = 3


symbol = "WEED.TO"
#symbol = "EMHTF"
#symbol = "PRMCF"
#symbol = "ACBFF"
#symbol = "MEDFF"
#symbol = "AMZN"

is_data_available, date_time_real, volume_real, opn_real, close_real, high_real, low_real = read.get_intraday_data(symbol, real_start_date, real_end_date, "1m")

if not (is_data_available):
    print "No real data available"
    exit(0)

predicted_prices, times, closest_date_times, distances = prediction.get_linear_interpolation_prediction(symbol, start_date, end_date, days_count, interp_count)

distance = analytics.get_distance(close_real, predicted_prices)

print distance

#print predicted_prices
#print times
#print closest_date_times
#print distances

#plt.plot(times, predicted_prices)
#plt.gcf().autofmt_xdate()

#plt.show()


