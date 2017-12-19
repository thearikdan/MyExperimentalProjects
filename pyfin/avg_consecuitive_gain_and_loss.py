from input import read
from stats import percentage, absolute
import numpy as np
from viz import bar
from utils import time, shape, string_op
from datetime import datetime
import dateutil



#name = '/home/ara/Downloads/PRMCF.csv'
#name = '/home/ara/Downloads/WEED.TO.csv'
#name = '/home/ara/Downloads/ACB.TO.csv'
#name = '/home/ara/Downloads/APHQF.csv'
#name = '/home/ara/Downloads/IVITF.csv'


#all_data = read.get_all_data_from_file(name)

#data = read.get_numeric_data_from_all_data(all_data)

symbol = "WEED.TO"
end_date = datetime.today() #today
start_date = end_date + dateutil.relativedelta.relativedelta(months=-1) #month ago

_, data = read.get_data_from_web(symbol, start_date, end_date)


change = absolute.get_absolute_change_from_numeric_data(data)

#print change

sh = np.shape(change)

POSITIVE_TYPE = 1
NEGATIVE_TYPE = -1
current_type = 0 

#consec_pos_day_gain = []
#consec_neg_day_loss = []
consec_day = []

pos_start = 0
pos_end = 0

neg_start = 0
neg_end = 0

count = 0


for i in range (sh[0]):
    #if positive day
    if (change[i][0] > 0):
        if current_type == POSITIVE_TYPE:
            count = count + 1
            continue
        elif current_type == NEGATIVE_TYPE:
            neg_end = read.get_closing_price_from_numeric_data(data[i-1:i])[0][0]
            record = np.array([neg_start, neg_end, count])
            consec_day.append(record)
 
            pos_start = read.get_opening_price_from_numeric_data(data[i:i+1])[0][0]
            count = 1
        else:
            pos_start = read.get_opening_price_from_numeric_data(data[i:i+1])[0][0]
            count = 1
        current_type = POSITIVE_TYPE
    else:
        if current_type == NEGATIVE_TYPE:
            count = count + 1
            continue
        elif current_type == POSITIVE_TYPE:
            pos_end = read.get_closing_price_from_numeric_data(data[i-1:i])[0][0]
            record = np.array([pos_start, pos_end, count])
            consec_day.append(record)

            neg_start = read.get_opening_price_from_numeric_data(data[i:i+1])[0][0]
            count = 1
        else:
            neg_start = read.get_opening_price_from_numeric_data(data[i:i+1])[0][0]
            count = 1
        current_type = NEGATIVE_TYPE


#append last end
if current_type == POSITIVE_TYPE:
    pos_end = read.get_closing_price_from_numeric_data(data[i:i+1])[0][0]
    record = np.array([pos_start, pos_end, count])
    consec_day.append(record)
else:
    neg_end = read.get_closing_price_from_numeric_data(data[i:i+1])[0][0]
    record = np.array([neg_start, neg_end, count])
    consec_day.append(record)

np_consec_day = np.array(consec_day)

#comp_name = string_op.get_company_name_from_file_name(name)
#title = comp_name + ": " + time.get_date_interval_text(date)
title = symbol + ": " + start_date.strftime("%Y-%m-%d")+ " to " + end_date.strftime("%Y-%m-%d")
bar.show(np_consec_day, title)
