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

mpc_max = percentage.get_max_percentage_change_from_numeric_data(nd)
mperc_max = mpc_max * 100

mpc_min = percentage.get_min_percentage_change_from_numeric_data(nd)
mperc_min = mpc_min * 100

sh = np.shape(perc)

pos_day_max_change = []
neg_day_max_change = []


for i in range (sh[0]):
    #if positive day
    if (perc[i][0] > 0):
        pos_day_max_change.append(mperc_max[i][0])
    else:
        neg_day_max_change.append(mperc_min[i][0])

print "One day maximum changes on positive days (%):"
print pos_day_max_change

print "One day average maximum changes on positive days (%):"
avg_pos_day_max_change = sum(pos_day_max_change) / len(pos_day_max_change)
print avg_pos_day_max_change

n_os_day_max_change = np.array(pos_day_max_change)
print "Standard deviation for one day average maximum changes on positive days:"
print np.std(n_os_day_max_change, axis=0)


print "One day maximum changes on negative days (%):"
print neg_day_max_change

print "One day average maximum changes on negative days (%):"
avg_neg_day_max_change = sum(neg_day_max_change) / len(neg_day_max_change)
print avg_neg_day_max_change

n_os_day_max_change = np.array(neg_day_max_change)
print "Standard deviation for one day average maximum changes on negative days:"
print np.std(n_os_day_max_change, axis=0)

