from datetime import datetime 
import dateutil
from utils import prediction
start_date = datetime(2018, 2, 2, 9, 30)
end_date = datetime(2018, 2, 2, 10, 30)

days_count = 15

DAYS_MAX_DEPTH = 30

ROOT_DIR = "results/analysis"

#names = ["tickers/cannabis.txt", "tickers/cannot_be_positive.txt", "tickers/cannot_be_negative.txt", "tickers/battery.txt"]
names = ["tickers/important.txt"]
#names = ["tickers/cannot_be_positive.txt"]



for name in names:
    with open(name) as f:
        tickers = f.read().splitlines()
        count = len(tickers)
        for i in range (count):
            for j in range (days_count):
                start_date = start_date + dateutil.relativedelta.relativedelta(days=-j) 
                end_date = end_date + dateutil.relativedelta.relativedelta(days=-j) 
                prediction.analyse_linear_interpolation_prediction_performance(tickers[i], start_date, end_date, DAYS_MAX_DEPTH, ROOT_DIR)



