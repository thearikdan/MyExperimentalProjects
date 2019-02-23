import sys
sys.path.insert(0, "../..")


from utils.stats import derivative

a = [0, 1, 2, 3, 6, 18]
interval = 1
a1 = derivative.get_derivative_list(a, interval)
print a1

if (a1 == [1.0, 1.0, 1.0, 3.0, 12.0]):
    print "Test succeeded"
else:
    print "Test failed"

interval = 2
a2 = derivative.get_derivative_list(a, interval)
print a2


if (a2 == [0.5, 0.5, 0.5, 1.5, 6.0]):
    print "Test succeeded"
else:
    print "Test failed"





