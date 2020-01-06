import requests
result = requests.get("http://www.cnn.com")
c = result.content

from bs4 import BeautifulSoup
soup = BeautifulSoup(c)
#soup = BeautifulSoup(c, "html.parser")

samples = soup.find_all("a", "data-analytics")
#samples = soup.find_all("a")

print (samples[0])

