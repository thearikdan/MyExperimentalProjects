'''
from read_write import read
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

#start_date = datetime(2018, 1, 5, 9, 30)
#end_date = datetime(2018, 1, 5, 15, 39)

start_date = datetime(2018, 4, 4, 9, 30)
end_date = datetime(2018, 4, 4, 15, 39)

is_data_available, date_time, volume , opn, close, high, low = read.get_intraday_data("NVDA", start_date, end_date, 1)

if not (is_data_available):
    exit(0)

plt.plot(date_time, close)
plt.gcf().autofmt_xdate()

plt.show()
'''

import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates

#if necessary convert to datetime
df.date = pd.to_datetime(df.date)

df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
df["date"] = df["date"].apply(mdates.date2num)

f1 = plt.subplot2grid((6, 4), (1, 0), rowspan=6, colspan=4, axisbg='#07000d')
candlestick_ohlc(f1, df.values, width=.6, colorup='#53c156', colordown='#ff1717')
f1.xaxis_date()
f1.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d %H:%M:%S'))

plt.xticks(rotation=45)
plt.ylabel('Stock Price')
plt.xlabel('Date Hours:Minutes')
plt.show()
