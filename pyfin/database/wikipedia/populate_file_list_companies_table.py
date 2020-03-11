import sys
sys.path.append("../..")

from utils.db import db
import json


def get_company_data_from_json_file(file_name):
    syms = []
    nams = []
    ipos = []
    secs = []
    inds = []
    quos = []
    mark = []
    suff = []

    with open(file_name, 'r') as infile:
        new_companies_data = json.load(infile)

    count = len(new_companies_data)
    for i in range(1, count):
        syms.append(new_companies_data[i]["symbol"])
        #Sanitize names
        nams.append(new_companies_data[i]["Company name"])
        ipos.append("n/a")
        secs.append("n/a")
        ind = new_companies_data[i]["Industry"]
        if ind == "":
            ind = "n/a"
        inds.append(ind)
        quos.append("n/a")
#        mark.append(1)
        mark.append(2)
        suff.append("")

    return syms, nams, ipos, secs, inds, quos, mark, suff




#syms, nams, ipos, secs, inds, quos, mark, suff = get_company_data_from_json_file("new_nasdaq_companies.json")
syms, nams, ipos, secs, inds, quos, mark, suff = get_company_data_from_json_file("new_nyse_companies.json")
print (syms, nams, ipos, secs, inds, quos, mark, suff)

conn, cursor = db.connect_to_database("../database_settings.txt")

db.insert_companies("public.companies", conn, cursor, syms, nams, ipos, secs, inds, quos, mark)


cursor.close()
conn.close()

