import lxml
from lxml import html
import requests
import time
import csv
import pandas as pd

symbol = "NFLX"
url = 'https://finance.yahoo.com/quote/' + symbol + '/balance-sheet?p=' + symbol
page = requests.get(url)
tree = html.fromstring(page.content)

# Using XPATH, fetch all table elements on the page
table = tree.xpath('//table') 
tstring = lxml.etree.tostring(table[0], method='html')
df = pd.read_html(tstring)[0]

print (df)
