import sys
sys.path.append("../..")

from utils import time_op
import datetime

times1 = [datetime.time(9, 43), datetime.time(9, 44)]
times1_str = time_op.get_postgresql_time_array_string(times1)

print times1_str


times2 = [datetime.time(9, 43)]
times2_str = time_op.get_postgresql_time_array_string(times2)

print times2_str



times3 = []
times3_str = time_op.get_postgresql_time_array_string(times3)

print times3_str

