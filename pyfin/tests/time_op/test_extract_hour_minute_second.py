import sys
sys.path.append("../..")

from utils import time_op
from datetime import datetime

dt = datetime(2018, 10, 2, 9, 30)
dt_ext = time_op.extract_hour_minute_second(dt)

print dt
print dt_ext

