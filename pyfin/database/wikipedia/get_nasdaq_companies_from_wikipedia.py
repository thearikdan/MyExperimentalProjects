import urllib.request as urllib2
from bs4 import BeautifulSoup


ROOT = "https://en.wikipedia.org/w/index.php?title=Category:Companies_listed_on_NASDAQ&from="

suffix_list = ['0']
letter_list = [chr(x) for x in range(ord('A'), ord('Z') + 1)]
suffix_list.extend(letter_list)

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

def get_companies_data(s, wiki_url):
    companies = []
    page = urllib2.urlopen(wiki_url)
    soup = BeautifulSoup(page,'html.parser')
    li = soup.find_all("li")
    for l in li:
        if is_category_company_li(s, l):
            companies.append(l.get_text())
    return companies


companies = []

for s in suffix_list:
    wiki_url = ROOT + s
    companies_s  = get_companies_data(s, wiki_url)
    companies.extend(companies_s)
print(companies)
print (len(companies))
