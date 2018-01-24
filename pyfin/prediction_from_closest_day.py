from datetime import datetime
from utils import prediction, interpolation
from stats import percentage
from read_write import read
import matplotlib.pyplot as plt




start_date = datetime(2018, 1, 24, 9, 30)
end_date = datetime(2018, 1, 24, 11, 50)

days_count = 30

symbol = "WEED.TO"
#symbol = "EMHTF"
#symbol = "PRMCF"
#symbol = "ACBFF"
#symbol = "MEDFF"
#symbol = "AMZN"


is_data_available, date_time_curr, volume_curr , opn_curr, close_curr, high_curr, low_curr = read.get_intraday_data(symbol, start_date, end_date, "1m")

if not (is_data_available):
    exit(0)

print close_curr
count_curr = len(close_curr)
last_price = close_curr[count_curr - 1]
print last_price

start, end, dist = prediction.get_closest_distances_time_to_predict_and_distances(symbol, start_date, end_date, days_count)

count = len(start)

date_time_per_list = []
volume_per_list = []
open_per_list = []
close_per_list = []
high_per_list = []
low_per_list = []

for i in range (count):
    is_data_available, date_time, volume , opn, close, high, low = read.get_intraday_data(symbol, start[i], end[i], "1m")
        
    if not (is_data_available):
        continue

    date_time_per, volume_per, open_per, close_per, high_per, low_per = percentage.get_percentage_change_in_intraday_prices(date_time, volume , opn, close, high, low)

    date_time_per_list.append(date_time_per)
    volume_per_list.append(volume_per)
    open_per_list.append(open_per)
    close_per_list.append(close_per)
    high_per_list.append(high_per)
    low_per_list.append(low_per)

count = len(date_time_per_list)
interp_count = 10

if (interp_count > count):
    interp_count = count

interp_volume_per, interp_open_per, interp_close_per, interp_high_per, interp_low_per = interpolation.interpolate_prices_and_volume_by_distance(volume_per_list, open_per_list, close_per_list, high_per_list, low_per_list, dist, interp_count)

#print interp_close_per

#print date_time_per_list[0]
#print len(date_time_per_list[0])

predicted_prices = prediction.project_percentage_change(last_price, interp_close_per)
#print len(predicted_prices)
#print predicted_prices

plt.plot(date_time_per_list[0], predicted_prices)
plt.gcf().autofmt_xdate()

plt.show()


