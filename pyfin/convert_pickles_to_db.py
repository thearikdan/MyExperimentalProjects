from utils import file_op
import os

DATA_DIR = "data"

dirs = {}
tickers = file_op.get_only_dirs(DATA_DIR)

ticker_count = len(tickers)
for i in range (ticker_count):
    dates = []
    subdir = os.path.join(DATA_DIR, tickers[i])
    d = file_op.get_only_dirs(subdir)
    dirs[tickers[i]] = d

print dirs


