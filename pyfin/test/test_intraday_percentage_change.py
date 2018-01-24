import sys
sys.path.insert(0, "../")


from stats import percentage

a = [1, 2, 3, 6, 18]
b = percentage.get_intraday_percentage_change(a)
print b

if (b == [1.0, 0.5, 1, 2]):
    print "Test succeeded"
else:
    print "Test failed"





