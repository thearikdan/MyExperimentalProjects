from datetime import datetime
from read_write import read
from stats import percentage

start_date = datetime(2018, 1, 26, 9, 30)
end_date = datetime(2018, 1, 26, 15, 59)


#symbol = "WEED.TO"
#symbol = "EMHTF"
#symbol = "PRMCF"
symbol = "ACBFF"
#symbol = "MEDFF"
#symbol = "AMZN"
#symbol = "DIS"

delta = 0.0001

is_data_available, date_time, volume, opn, close, high, low = read.get_intraday_data(symbol, start_date, end_date, 1)

if not (is_data_available):
    print ("No ground truth data available")
    exit(0)


per_list = percentage.get_intraday_percentage_change(close)
count = len(per_list)

print per_list

start = -0.1
end = 0.1

bag_count = int ((end - start) / delta)
print bag_count

bag = [0] * bag_count

for i in range (count):
    for j in range (bag_count):
        if ((per_list[i] >= start + j * delta) and (per_list[i] < start + (j + 1 ) * delta)):
            bag[j] = bag[j] + 1
            continue

print bag
     


