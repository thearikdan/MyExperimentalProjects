import json
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument("-i", "--input_json_file", required=True, help="Specify the name of the input json file")
parser.add_argument("-e", "--existing_industries_csv", required=True, help="List of existing industries exported from database")
parser.add_argument("-o", "--output_txt_file", required=True, help="Specify the name of the output txt file with names of new industries")


args = parser.parse_args()
params = vars(args)

#new_dict_file_name = "new_nasdaq_companies.json"
#new_dict_file_name = "new_nyse_companies.json"
new_dict_file_name = params['input_json_file']

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

#ind_file_name = 'industries_db.csv'
ind_file_name = params['existing_industries_csv']
with open(ind_file_name, 'r') as f:
    existing_industries = f.read().splitlines()

print (existing_industries)

new_industries = []
for ind in industries:
    if not ind in existing_industries:
        new_industries.append(ind)

print (new_industries)

#out_file_name = 'new_industries.txt'
out_file_name = params['output_txt_file']
with open(out_file_name, 'w') as f:
    for ind in new_industries:
        f.write("%s\n" % ind)