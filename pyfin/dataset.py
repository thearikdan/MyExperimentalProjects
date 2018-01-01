from read_write import read
from datetime import datetime

N = 5
now = datetime.now()
read.get_all_intraday_prices_for_N_days_to_date ("WEED_TO", N,now)


