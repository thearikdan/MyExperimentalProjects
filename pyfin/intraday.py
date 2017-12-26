#https://stackoverflow.com/questions/44030983/yahoo-finance-url-not-working
#https://query1.finance.yahoo.com/v8/finance/chart/WEED.TO?interval=1m

import urllib2
import json

def get_intraday_data(symbol, interval):
    str = "https://query1.finance.yahoo.com/v8/finance/chart/%s?interval=%s" % (symbol, interval)
    response = urllib2.urlopen(str).read()
    json_obj = json.loads(response)

    chart = (json_obj['chart'])
    result = chart['result']
    indicators = result[0]['indicators']
    quote = indicators['quote']

    high = quote[0]['high']
    low = quote[0]['low']
    open = quote[0]['open']
    close = quote[0]['close']
    volume = quote[0]['volume']

    timestamp = result[0]['timestamp']
    return timestamp, volume, open, close, high, low


timestamp, volume , open, close, high, low = get_intraday_data("WEED.TO", "1m")
print open

