from read_write import read
from datetime import datetime
import time

N = 365
now = datetime.now()

start_time = time.time()

read.get_all_intraday_prices_for_N_days_to_date ("WEED_TO", N, now)

elapsed_time = time.time() - start_time

print elapsed_time

#29.4082150459 seconds for 1 year


