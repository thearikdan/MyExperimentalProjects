import json

data  = ["a", "b", "c"]

with open('data.json', 'w') as outfile:
    json.dump(data, outfile)

with open('data.json', 'r') as infile:
    data = json.load(infile)
    print data


