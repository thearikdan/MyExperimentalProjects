import sys
sys.path.insert(0, "../")


from stats import absolute
from datetime import datetime, timedelta


count = 10

start_time = datetime(2000, 1, 1, 10, 00, 00)
start_volume = 1000
opn = 20
close = 21

time_list = []
volume_list = []
opn_list = []
close_list = []
high_list = [21, 25, 19, 22, 26, 22, 18, 23, 28, 23]
low_list =  [19, 17, 15, 18, 13, 15, 19, 21, 14, 15]


for i in range (count):
    time_list.append(start_time + timedelta(minutes = i))
    volume_list.append(start_volume + 100 * i)
    opn_list.append(opn + i)
    close_list.append(close + i)


t1, v1, o1, c1, h1, l1 = absolute.get_N_minute_from_one_minute_interval(1, time_list, volume_list , opn_list, close_list, high_list, low_list)

if (t1 != time_list):
    print "One minute time test failed"
else:
    print "One minute time test succeeded"

if (v1 != volume_list):
    print "One minute volume test failed"
else:
    print "One minute volume test succeeded"

if (o1 != opn_list):
    print "One minute open test failed"
else:
    print "One minute open test succeeded"

if (c1 != close_list):
    print "One minute close test failed"
else:
    print "One minute close test succeded"

if (h1 != high_list):
    print "One minute high test failed"
else:
    print "One minute high test succeded"

if (l1 != low_list):
    print "One minute low test failed"
else:
    print "One minute low test succeded"


t3, v3, o3, c3, h3, l3 = absolute.get_N_minute_from_one_minute_interval(3, time_list, volume_list , opn_list, close_list, high_list, low_list)

if (t3 != [datetime(2000, 1, 1, 10, 00, 00), datetime(2000, 1, 1, 10, 3), datetime(2000, 1, 1, 10, 6)]):
    print "Three minutes time test failed"
else:
    print "Three minutes time test succeeded"

if (o3 != [20, 23, 26]):
    print "Three minutes open test failed"
else:
    print "Three minutes open test succeeded"

if (c3 != [21, 24, 27]):
    print "Three minutes close test failed"
else:
    print "Three minutes close test succeeded"

if (h3 != [25, 26, 28]):
    print "Three minutes high test failed"
else:
    print "Three minutes high test succeeded"

if (l3 != [15, 13, 14]):
    print "Three minutes low test failed"
else:
    print "Three minutes low test succeeded"



