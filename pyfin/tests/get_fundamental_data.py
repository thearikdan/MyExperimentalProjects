#from https://stackoverflow.com/questions/40139537/scrape-yahoo-finance-financial-ratios
#pip install requests
import requests

params = {"formatted": "true",
        "crumb": "AKV/cl0TOgz", # works without so not sure of significance
        "lang": "en-US",
        "region": "US",
        "modules": "defaultKeyStatistics,financialData,calendarEvents",
        "corsDomain": "finance.yahoo.com"}

r = requests.get("https://query1.finance.yahoo.com/v10/finance/quoteSummary/AMZN", params=params)
data = r.json()[u'quoteSummary']["result"][0]
print data
