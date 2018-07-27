from datetime import datetime
from utils import prediction
import matplotlib.pyplot as plt


start_date = datetime(2018, 7, 27, 9, 30)
end_date = datetime(2018, 7, 27, 13, 20)

days_count = 15

interp_count = 3


#symbol = "WEED.TO"
#symbol = "EMHTF"
#symbol = "PRMCF"
#symbol = "ACBFF"
#symbol = "MEDFF"
symbol = "AMZN"

predicted_prices, times, closest_date_times, distances = prediction.get_linear_interpolation_prediction("data", symbol, start_date, end_date, days_count, interp_count)

print closest_date_times
print distances

plt.plot(times, predicted_prices)
plt.gcf().autofmt_xdate()

plt.show()


