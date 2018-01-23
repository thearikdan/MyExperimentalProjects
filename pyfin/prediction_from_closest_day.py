from datetime import datetime
from utils import prediction
from stats import percentage
from read_write import read

start_date = datetime(2018, 1, 22, 9, 30)
end_date = datetime(2018, 1, 22, 10, 30)

days_count = 18

symbol = "WEED.TO"
#symbol = "EMHTF"
#symbol = "PRMCF"
#symbol = "ACBFF"
#symbol = "MEDFF"
#symbol = "AMZN"

start, end, dist = prediction.get_closest_distance_time_to_predict_and_distance(symbol, start_date, end_date, days_count)
print start, end, dist

is_data_available, date_time, volume , opn, close, high, low = read.get_intraday_data(symbol, start, end, "1m")
        
if not (is_data_available):
    exit(0)

date_time_per, volume_per , open_per, close_per, high_per, low_per = percentage.get_percentage_change_in_intraday_prices(date_time, volume , opn, close, high, low)

print date_time_per
print close_per
