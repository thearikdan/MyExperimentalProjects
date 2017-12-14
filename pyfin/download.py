import pandas_datareader as pdr
from datetime import datetime
import dateutil

#datetime format is year, month, day

def get_data(ticker, start_date, end_date):
    data = pdr.get_data_yahoo(symbols=ticker, start=start_date, end=end_date)
#    return(data['Open'], data['High'], data['Adj Close'])
    return data.as_matrix()

symbol = "IBM"
today = datetime.today()
month_ago = today + dateutil.relativedelta.relativedelta(months=-1)

print get_data(symbol, month_ago, today)

