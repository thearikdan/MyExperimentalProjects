from datetime import datetime
from utils import prediction
start_date = datetime(2018, 1, 24, 9, 30)
end_date = datetime(2018, 1, 24, 10, 30)

DAYS_TO_ANALYSE = 30

ROOT_DIR = "results/analysis"

names = ["tickers/cannabis.txt", "tickers/cannot_be_positive.txt", "tickers/cannot_be_negative.txt", "tickers/battery.txt"]


for name in names:
    with open(name) as f:
        tickers = f.read().splitlines()
        count = len(tickers)
        for i in range (count):
            prediction.analyse_linear_interpolation_prediction_performance(tickers[i], start_date, end_date, DAYS_TO_ANALYSE, ROOT_DIR)



