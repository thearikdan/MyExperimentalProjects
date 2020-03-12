import json
from argparse import ArgumentParser
import sys


#The script assumes json file was created by get_companies_from_wiki.py script
#json_file_name = "NasdaqCompanies-Mar-03-2020.json"
#It also assumes the list of existing companies from the stock exchange is exported into csv file
#existing_companies_csv = 'nyse_existing_db.csv'

def get_industry(dict):
    try:
        industry = dict["Industry"]
        return (industry)
    except:
        return ""


def get_symbol_from_traded(traded, stock_exchange):
    splt = traded.split()[0]
    splt = splt.split(":")[1]
    splt = splt.split("(")[0]
    splt = splt.split("S&P")[0]
    splt = splt.split("NASDAQ")[0]
    splt = splt.split("NYSE")[0]
    splt = splt.split(")")[0]
    splt = splt.split("[")[0]
    splt = splt.split("Russel")[0]
    splt = splt.split("Alternext")[0]
    splt = splt.split("TSX")[0]
    splt = splt.split(",")[0]
    splt = splt.split("DJTA")[0]
    splt = splt.split("DJUA")[0]
    splt = splt.split("DJIA")[0]
    splt = splt.split("SEHK")[0]
    splt = splt.split("TANDER")[0]
    splt = splt.split("DJIAcomponent")[0]
    splt = splt.split("DJUA")[0]
    splt = splt.split("Euronext")[0]
    splt = splt.split("Class")[0]
    splt = splt.split(".VCommon")[0]
    if stock_exchange == "LSE":
        splt = splt.split("LSE")[0]
        splt = splt.split("FWB")[0]
        splt = splt.split("FTSE")[0]
        splt = splt.split("SGX")[0]
        splt = splt.split("MCX")[0]
        splt = splt.rstrip('.')
    return splt


parser = ArgumentParser()

parser.add_argument("-i", "--input_json_file", required=True, help="Specify the name of the input json file")
parser.add_argument("-x", "--stock_exchange_name", required=True, help="Specify the name of the stock exchange")
parser.add_argument("-e", "--existing_companies_csv", required=True, help="List of existing companies of the stock exchange exported from database")
parser.add_argument("-o", "--output_json_file", required=True, help="Specify the name of the output json file with names of new companies")


args = parser.parse_args()
params = vars(args)

#input_json_file_name = "NYSECompanies-Mar-10-2020.json"
input_json_file_name  = params['input_json_file']

#stock_exchange = "NASDAQ"
#stock_exchange = "NYSE"
#stock_exchange = "LSE"
stock_exchange = params['stock_exchange_name']

#new_companies_file_name = "new_nyse_companies.json"
new_companies_file_name = params['output_json_file']

#existing_companies_csv = 'nyse_existing_db.csv'
existing_companies_csv = params['existing_companies_csv']


with open(input_json_file_name, 'r') as infile:
    companies_data = json.load(infile)

#print (companies_data)

names = []
industries = []
nasdaq_data = []
for dict in companies_data:
    try:
        name = dict["Company name"]
        traded = dict["Traded\xa0as"]
        symbol = get_symbol_from_traded(traded, stock_exchange)
        if symbol == "":
            continue
        industry = get_industry(dict)
#        if "NASDAQ:" in traded:
        if stock_exchange in traded:
            nasdaq_data.append(symbol)
            industries.append(industry)
            names.append(name)
    except:
        continue


existing_companies = []
#with open('nasdaq_existing_db.csv', 'r') as f:
with open(existing_companies_csv, 'r') as f:
    existing_companies = f.read().splitlines()

#print(existing_companies)

wiki_count = len(names)
new_dict_list = []
for i in range (wiki_count):
    if not nasdaq_data[i] in existing_companies:
        new_dict = {}
        new_dict["Company name"] = names[i]
        new_dict["symbol"] = nasdaq_data[i]
        new_dict["Industry"] = industries[i]
        new_dict_list.append(new_dict)
        print (new_dict)


with open(new_companies_file_name, 'w') as outfile:
    json.dump(new_dict_list, outfile)

