import sys
sys.path.append("../..")

from utils import time_op

N= 5
days = time_op.get_last_N_days_list_from_now(N)
print days
print len(days)
