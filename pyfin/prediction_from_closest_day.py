from datetime import datetime
from utils import prediction

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

