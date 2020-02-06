import urllib.request as urllib2
from bs4 import BeautifulSoup

ICCV_2019='http://openaccess.thecvf.com/ICCV2019.py'

page = urllib2.urlopen(ICCV_2019)
soup = BeautifulSoup(page,'html.parser')

dt_ptitle = soup.find_all('dt', {"class":"ptitle"})
titles = []
for dt in dt_ptitle:
    titles.append(dt.get_text())

print (titles)