#https://stackoverflow.com/questions/44030983/yahoo-finance-url-not-working
#https://query1.finance.yahoo.com/v8/finance/chart/WEED.TO?interval=1m

import urllib2
import json

response = urllib2.urlopen("https://query1.finance.yahoo.com/v8/finance/chart/WEED.TO?interval=1m").read()
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


print high

