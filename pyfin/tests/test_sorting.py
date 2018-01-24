import sys
sys.path.insert(0, "../")


from utils import sort_op

a = [4, 3, 7, 1, 8, 9, 5, 0]
b = sort_op.get_sorted_indices(a)

print b

if (b == [7, 3, 1, 0, 6, 2, 4, 5]):
    print "Test succeeded"
else:
    print "Test failed"


