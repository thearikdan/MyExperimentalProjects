import pandas_datareader as pdr
from datetime import datetime
import dateutil

ticker = "IBM"
today = datetime.today()
print today 

yesterday = today + dateutil.relativedelta.relativedelta(days=-1)
print yesterday

month_ago = today + dateutil.relativedelta.relativedelta(months=-1)
print month_ago

#ibm = pdr.get_data_yahoo(symbols=ticker, start=yesterday, end=month_ago)
#print(ibm['Adj Close'])

ibm = pdr.get_data_yahoo(symbols=ticker, start=datetime(2017, 12, 13), end=datetime(2017, 11, 14))
print(ibm['Adj Close'])

