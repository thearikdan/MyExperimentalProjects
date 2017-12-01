from input import read
from stats import percentage 
import numpy as np



#name = '/raid/data/pyfin/LEAF.TO.csv'
#name = '/raid/data/pyfin/AMZN.csv'

#name = '/media/ara/HDD/data/Finance/ACB.TO.csv'
name = '/media/ara/HDD/data/Finance/WEED.TO_1_month.csv'
#name = '/media/ara/HDD/data/Finance/AMZN_month.csv'


data = read.get_all_data_from_file(name)

date = read.get_date_from_all_data(data)
sh = np.shape(date)

nd = read.get_numeric_data_from_all_data(data)

pc = percentage.get_percentage_change_from_numeric_data(nd)
perc = pc * 100

sh = np.shape(perc)

POSITIVE_TYPE = 1
NEGATIVE_TYPE = -1
current_type = 0 

cons_pos_day_num = []
cons_neg_day_num = []

count = 0
for i in range (sh[0]):
    #if positive day
    if (perc[i][0] > 0):
        if current_type == POSITIVE_TYPE:
            count = count + 1
        elif current_type == NEGATIVE_TYPE:
            cons_neg_day_num.append(count)
            count = 1
        current_type = POSITIVE_TYPE
    else:
        if current_type == NEGATIVE_TYPE:
            count = count + 1
        elif current_type == POSITIVE_TYPE:
            cons_pos_day_num.append(count)
            count = 1
        current_type = NEGATIVE_TYPE

print "Consequtive positive days (%):"
print cons_pos_day_num

print "Average number consequtive positive days (%):"
avg_con_pos_days = sum(cons_pos_day_num) / len(cons_pos_day_num)
print avg_con_pos_days


print "Consequtive negative days (%):"
print cons_neg_day_num

print "Average number consequtive negative days (%):"
avg_con_neg_days = sum(cons_neg_day_num) / len(cons_neg_day_num)
print avg_con_neg_days

