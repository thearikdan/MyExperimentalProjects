import requests
from bs4 import BeautifulSoup

#result = requests.get("https://finance.yahoo.com/quote/NFLX?p=NFLX")
result = requests.get("https://www.reuters.com/search/news?blob=netflix&sortBy=relevance&dateRange=pastWeek")
c = result.content
print (c)
soup = BeautifulSoup(c)
