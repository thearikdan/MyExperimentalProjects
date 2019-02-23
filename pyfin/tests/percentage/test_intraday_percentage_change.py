import sys
sys.path.insert(0, "../..")


from utils.stats import percentage

a = [0, 1, 2, 3, 6, 18]
b = percentage.get_percentage_change_in_list(a)
print b

if (b == [0.0, 1.0, 0.5, 1, 2]):
    print "Test succeeded"
else:
    print "Test failed"





