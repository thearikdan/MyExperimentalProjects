import sys
sys.path.insert(0, "../")

from utils import heal

a = [1.0, 2,0, None, 0.0, 8.7]
print a

ratio = heal.get_corrupt_ratio(a)
print ratio

if (ratio == 1.0 / len(a)):
    print "Test passed"
else:
    print "Test failed"

