import sys
sys.path.insert(0, "../")


from utils import analytics

a = [0, 1]
b = [0, 1]

c = analytics.get_distance(a, b)
print c

if (c == 0):
    print "Test1 succeeded"
else:
    print "Test1 failed"


a = [0, 1]
b = [1, 0]

c = analytics.get_distance(a, b)
print c

if (abs (c - 1.41421356237) < 0.0001):
    print "Test2 succeeded"
else:
    print "Test2 failed"



a = [0, 1]
b = [0, -1]

c = analytics.get_distance(a, b)
print c

if (c == 2):
    print "Test3 succeeded"
else:
    print "Test3 failed"



