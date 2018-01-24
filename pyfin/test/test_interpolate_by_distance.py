import sys
sys.path.insert(0, "../")


from utils import interpolation

a = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]
weights = [0.1, 0.2]

b = interpolation.interpolate_by_distance(a, weights, 1)
print b

if (b == [1, 2, 3, 4, 5]):
    print "Test1 succeeded"
else:
    print "Test1 failed"


c = interpolation.interpolate_by_distance(a, weights, 2)
print c

if (c == [2.6666666666666665, 3.666666666666666, 4.666666666666666, 5.666666666666666, 6.666666666666666]):
    print "Test2 succeeded"
else:
    print "Test2 failed"


d = interpolation.interpolate_by_distance(a, weights, 3)
print d

if (d == [2.6666666666666665, 3.666666666666666, 4.666666666666666, 5.666666666666666, 6.666666666666666]):
    print "Test3 succeeded"
else:
    print "Test3 failed"



