from datetime import datetime, timedelta
from utils import prediction
import matplotlib.pyplot as plt
from read_write import read


start_date = datetime(2018, 1, 26, 9, 30)
end_date = datetime(2018, 1, 26, 10, 30)

days_count = 10

interp_count = 1


#symbol = "WEED.TO"
#symbol = "EMHTF"
#symbol = "PRMCF"
#symbol = "ACBFF"
#symbol = "MEDFF"
#symbol = "AMZN"
symbol = "DIS"


real_start_date = end_date + timedelta(minutes = 1)
real_end_date = end_date.replace(hour=15, minute=59)

is_data_available, date_time_real, volume_real, opn_real, close_real, high_real, low_real = read.get_intraday_data(symbol, real_start_date, real_end_date, "1m")

if not (is_data_available):
    print ("No ground truth data available")
    exit(0)


predicted_prices, times, closest_date_times, distances = prediction.get_linear_interpolation_prediction(symbol, start_date, end_date, days_count, interp_count)

print closest_date_times
print distances

plt.plot(times, predicted_prices)
plt.plot(times, close_real, 'r')

plt.gcf().autofmt_xdate()

plt.show()


