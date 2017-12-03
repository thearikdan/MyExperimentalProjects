from input import read
from stats import percentage, absolute
import numpy as np



#name = '/raid/data/pyfin/LEAF.TO.csv'
#name = '/raid/data/pyfin/AMZN.csv'

#name = '/media/ara/HDD/data/Finance/ACB.TO.csv'
name = '/media/ara/HDD/data/Finance/WEED.TO_1_month.csv'
#name = '/media/ara/HDD/data/Finance/AMZN_month.csv'


all_data = read.get_all_data_from_file(name)
print all_data

data = read.get_numeric_data_from_all_data(all_data)

date = read.get_date_from_all_data(data)
sh = np.shape(date)

change = absolute.get_absolute_change_from_numeric_data(data)

print change

sh = np.shape(change)

POSITIVE_TYPE = 1
NEGATIVE_TYPE = -1
current_type = 0 

consec_pos_day_gain = []
consec_neg_day_loss = []

pos_start = 0
pos_end = 0

neg_start = 0
neg_end = 0

#count = 0
for i in range (sh[0]):
    #if positive day
    if (change[i][0] > 0):
        if current_type == POSITIVE_TYPE:
            continue
        elif current_type == NEGATIVE_TYPE:
            neg_end = read.get_closing_price_from_numeric_data(data[i-1:i])[0][0]
            print "neg_end"
            print neg_end
            consec_neg_day_loss.append(neg_end - neg_start)
 
            pos_start = read.get_opening_price_from_numeric_data(data[i:i+1])[0][0]
            print "pos_start"
            print pos_start
        else:
            pos_start = read.get_opening_price_from_numeric_data(data[i:i+1])[0][0]
            print "pos_start"
            print pos_start
        current_type = POSITIVE_TYPE
    else:
        if current_type == NEGATIVE_TYPE:
            continue
        elif current_type == POSITIVE_TYPE:
            pos_end = read.get_closing_price_from_numeric_data(data[i-1:i])[0][0]
            print "pos_end"
            print pos_end
            consec_pos_day_gain.append(pos_end - pos_start)

            neg_start = read.get_opening_price_from_numeric_data(data[i:i+1])[0][0]
            print "neg_start"
            print neg_start
        else:
            neg_start = read.get_opening_price_from_numeric_data(data[i:i+1])[0][0]
            print "neg_start"
            print neg_start
        current_type = NEGATIVE_TYPE

print consec_pos_day_gain
print consec_neg_day_loss

#append last group
#if current_type == POSITIVE_TYPE:
#    cons_pos_day_num.append(count)
#else:
#    cons_neg_day_num.append(count)


#print "Consequtive positive days (%):"
#print cons_pos_day_num


#print "Total number positive days (%):"
#tot = sum(cons_pos_day_num) 
#print tot


#print "Average number consequtive positive days (%):"
#avg_con_pos_days = sum(cons_pos_day_num) / len(cons_pos_day_num)
#print avg_con_pos_days


#print "Consequtive negative days (%):"
#print cons_neg_day_num

#print "Total number negative days (%):"
#tot = sum(cons_neg_day_num) 
#print tot

#print "Average number consequtive negative days (%):"
#avg_con_neg_days = sum(cons_neg_day_num) / len(cons_neg_day_num)
#print avg_con_neg_days

