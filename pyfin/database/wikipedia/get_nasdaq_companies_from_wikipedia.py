import urllib.request as urllib2
from bs4 import BeautifulSoup



WIKI_URL_ROOT = "https://en.wikipedia.org"
WIKI_NASDAQ_ROOT = WIKI_URL_ROOT+"/w/index.php?title=Category:Companies_listed_on_NASDAQ&from="

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


def get_url_from_li(wiki_url_root, li):
    try:
        a = li.find(href=True)
        href = a['href']
        url = wiki_url_root + href
        return url
    except:
        return ""


def get_companies_data(s, wiki_url_root, wiki_nasdaq_url):
    companies = []
    company_wiki_urls = []
    page = urllib2.urlopen(wiki_nasdaq_url)
    soup = BeautifulSoup(page,'html.parser')
    lis = soup.find_all("li")
    for li in lis:
        if is_category_company_li(s, li):
            url = get_url_from_li(wiki_url_root, li)
            if len(url) > 0:
                companies.append(li.get_text())
                company_wiki_urls.append(url)
    return companies, company_wiki_urls


companies = []
wiki_company_uls = []

for s in suffix_list:
    wiki_nasdaq_url = WIKI_NASDAQ_ROOT + s
    companies_s, url_s  = get_companies_data(s, WIKI_URL_ROOT, wiki_nasdaq_url)
    companies.extend(companies_s)
    wiki_company_uls.extend(url_s)
print(companies)
print(wiki_company_uls)
print (len(companies))
