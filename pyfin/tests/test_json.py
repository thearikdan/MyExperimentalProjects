import json
from datetime import datetime

filename = "json_test.json"
data = [{"age":20, "sex":"male", "occupation":"student", "time":datetime(2020, 5, 1, 9).strftime("%m/%d/%Y, %H:%M:%S")}, {"age":26, "sex":"female", "occupation":"engineer", "time":datetime(2020, 5, 1, 9).strftime("%m/%d/%Y, %H:%M:%S")}, {"age":30, "sex":"male", "occupation":"manager", "time":datetime(2020, 5, 1, 10, 00).strftime("%m/%d/%Y, %H:%M:%S")}]

with open (filename, "w") as f:
    json.dump(data, f)


with open (filename, "r") as f:
    d = json.load(f)
    print (d)

