import sys
sys.path.insert(0, "../")


from utils import prediction

a = 10
b = [0.2, 0.5, -0.1, 0.05]

c = prediction.project_percentage_change(a, b)
print c

if (c == [12.0, 18.0, 16.2, 17.01]):
    print "Test succeeded"
else:
    print "Test failed"


