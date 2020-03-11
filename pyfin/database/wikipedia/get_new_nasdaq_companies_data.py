import json

#The script assumes json file was created by get_nasdaq_companies_from_wikipedia.py script
#json_file_name = "NasdaqCompanies-Mar-03-2020.json"
json_file_name = "NYSECompanies-Mar-10-2020.json"

def get_industry(dict):
    try:
        industry = dict["Industry"]
        return (industry)
    except:
        return ""


def get_symbol_from_traded(traded):
    splt = traded.split()[0]
    splt = splt.split(":")[1]
    splt = splt.split("(")[0]
    splt = splt.split("S&P")[0]
#    splt = splt.split("NASDAQ")[0]
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
    return splt


with open(json_file_name, 'r') as infile:
    companies_data = json.load(infile)

#print (companies_data)

names = []
industries = []
nasdaq_data = []
for dict in companies_data:
    try:
        name = dict["Company name"]
        traded = dict["Traded\xa0as"]
        symbol = get_symbol_from_traded(traded)
        if symbol == "":
            continue
        industry = get_industry(dict)
#        if "NASDAQ:" in traded:
        if "NYSE:" in traded:
            nasdaq_data.append(symbol)
            industries.append(industry)
            names.append(name)
    except:
        continue

#print (nasdaq_data)
#print(names)
#print(industries)


existing_companies = []
#with open('nasdaq_existing_db.csv', 'r') as f:
with open('nyse_existing_db.csv', 'r') as f:
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


#new_companies_file_name = "new_nasdaq_companies.json"
new_companies_file_name = "new_nyse_companies.json"
with open(new_companies_file_name, 'w') as outfile:
    json.dump(new_dict_list, outfile)

