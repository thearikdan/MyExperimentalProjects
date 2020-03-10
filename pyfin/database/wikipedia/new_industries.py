import json

new_dict_file_name = "new_nasdaq_companies.json"

with open(new_dict_file_name, 'r') as infile:
    new_companies_data = json.load(infile)


print (new_companies_data)

industries = []

for dct in new_companies_data:
    ind = dct["Industry"]
    if (ind == ""):
        ind = "n/a"
    industries.append(ind)


existing_industries = []
with open('industries_db.csv', 'r') as f:
    existing_industries = f.read().splitlines()

print (existing_industries)

new_industries = []
for ind in industries:
    if not ind in existing_industries:
        new_industries.append(ind)

print (new_industries)

with open('new_industries.txt', 'w') as f:
    for ind in new_industries:
        f.write("%s\n" % ind)