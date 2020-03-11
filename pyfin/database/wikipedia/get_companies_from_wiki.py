import urllib.request as urllib2
from bs4 import BeautifulSoup
import json
from datetime import date
from argparse import ArgumentParser
import sys


def print_usage():
    print ("Usage: python download_intraday_dataset.py -e stock exchange extension url -o output json file name")


def is_category_company_li(cat, li):
    letters_range = range (ord('A'), ord('Z') + 1)
    digits_range = range (ord('0'), ord('9') + 1)
    txt = li.get_text()
    if len(txt) == 0:
        return False
    a = li.find("a", {"class":"external text"})
    if a is not None:
        return False
    if ord(cat) in letters_range:
        if txt[0] == cat:
            return True
    if (cat == "0"):
        if ord(txt[0]) in digits_range:
            return True
    return False


def get_url_from_li(wiki_url_root, li):
    try:
        a = li.find(href=True)
        href = a['href']
        url = wiki_url_root + href
        return url
    except:
        return ""



def get_company_data_from_wiki_page(name, url):
    #https: // stackoverflow.com / questions / 54120864 / scraping - wikipedia - infobox - when - table - cells - are - in -mixed - formats
    info = {}
    try:
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page,'html.parser')
        tbl = soup.find("table", {"class": "infobox vcard"})
        list_of_table_rows = tbl.findAll('tr')
        for tr in list_of_table_rows:
            th = tr.find("th")
            td = tr.find("td")
            if th is not None:
                innerText = ''
                for elem in td.recursiveChildGenerator():
                    if isinstance(elem, str):
                        innerText += elem.strip()
                    elif elem.name == 'br':
                        innerText += '\n'
                info[th.text] = innerText
        info["Company name"] = name
        info["Wiki URL"] = url
        print(json.dumps(info, indent=1))
        return info
    except:
        return info



def get_companies_data(s, wiki_url_root, wiki_nasdaq_url):
    companies = []
    company_wiki_urls = []
    companies_data = []
    page = urllib2.urlopen(wiki_nasdaq_url)
    soup = BeautifulSoup(page,'html.parser')
    lis = soup.find_all("li")
    for li in lis:
        if is_category_company_li(s, li):
            url = get_url_from_li(wiki_url_root, li)
            if len(url) > 0:
                name = li.get_text()
                companies.append(name)
                company_wiki_urls.append(url)
                data = get_company_data_from_wiki_page(name, url)
                companies_data.append(data)
    return companies, company_wiki_urls, companies_data


parser = ArgumentParser()

parser.add_argument("-e", "--exchange_extension", required=True, help="Specify exchange specific url extension")
parser.add_argument("-o", "--output_file", required=True, help="Specify output file name")


args = parser.parse_args()

params = vars(args)
print (len(sys.argv))

if len(sys.argv) != 5:
    print_usage()
    exit()




WIKI_URL_ROOT = "https://en.wikipedia.org"
WIKI_EXCHANGE_EXTENSION = params['exchange_extension']

#WIKI_NASDAQ_ROOT = WIKI_URL_ROOT+"/w/index.php?title=Category:Companies_listed_on_NASDAQ&from="
#WIKI_NYSE_ROOT = "/w/index.php?title=Category:Companies_listed_on_the_New_York_Stock_Exchange&from="
#WIKI_NYSE_ROOT =  WIKI_URL_ROOT+WIKI_EXCHANGE_EXTENSION


WIKI_URL = WIKI_URL_ROOT + WIKI_EXCHANGE_EXTENSION
print(WIKI_URL)

suffix_list = ['0']
letter_list = [chr(x) for x in range(ord('A'), ord('Z') + 1)]
suffix_list.extend(letter_list)

companies = []
wiki_company_uls = []
companies_data = []

today = date.today()
today_str = today.strftime("%b-%d-%Y")
#json_file_name = "NasdaqCompanies-%s.json" % today_str
output_file = params['output_file']
print(output_file)
json_file_name = (output_file + "-%s.json") % today_str


for s in suffix_list:
#    wiki_nasdaq_url = WIKI_NASDAQ_ROOT + s
    wiki_nasdaq_url = WIKI_URL + s
    print(wiki_nasdaq_url)
    companies_s, url_s, data_s  = get_companies_data(s, WIKI_URL_ROOT, wiki_nasdaq_url)
    companies.extend(companies_s)
    wiki_company_uls.extend(url_s)
    companies_data.extend(data_s)
    print(data_s)

with open(json_file_name, 'w') as outfile:
    json.dump(companies_data, outfile)

print ("Number of companies: " + str(len(companies)))

