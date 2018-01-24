import sys
sys.path.insert(0, "../")


from stats import absolute

a = [1, 2, 3, 6, 5, 3, 1, 4, 7, 8, 6, 3, 2, 4, 6]

b = absolute.get_local_maximum_index_list(a, 2)
print b

if (b == [3, 9]):
    print "Local Maximum Test succeeded"
else:
    print "Local Maximum Test failed"


c = absolute.get_local_minimum_index_list(a, 2)
print c

if (c == [6, 12]):
    print "Local Minimum Test succeeded"
else:
    print "Local Minimum Test failed"





