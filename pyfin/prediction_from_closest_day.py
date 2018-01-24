from datetime import datetime
from utils import prediction
import matplotlib.pyplot as plt


start_date = datetime(2018, 1, 24, 9, 30)
end_date = datetime(2018, 1, 24, 15, 30)

days_count = 30

interp_count = 3


symbol = "WEED.TO"
#symbol = "EMHTF"
#symbol = "PRMCF"
#symbol = "ACBFF"
#symbol = "MEDFF"
#symbol = "AMZN"

predicted_prices, times, closest_date_times, distances = prediction.get_linear_interpolation_prediction(symbol, start_date, end_date, days_count, interp_count)

print predicted_prices
print times
print closest_date_times
print distances

plt.plot(times, predicted_prices)
plt.gcf().autofmt_xdate()

plt.show()


