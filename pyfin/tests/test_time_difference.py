import sys
sys.path.append("..")

from utils import time_op
from datetime import datetime, timedelta

t1 = datetime(2002, 12, 31, 9, 30)
t2 = datetime(2002, 12, 31, 16, 00)

hours, minutes, seconds = time_op.get_number_of_hours_minutes_seconds_between_times(t1, t2)
print (hours, minutes, seconds)

minutes, seconds = time_op.get_number_of_minutes_seconds_between_times(t1, t2)
print (minutes, seconds)

seconds = time_op.get_number_of_seconds_between_times(t1, t2)
print (seconds)
