import sys
sys.path.append("..")

from utils import file_op, db
import psycopg2
import os

DATA_DIR = "../downloads/eodata_list"


def get_market_and_suffix_from_file(market_file):

    suffix_dict = {'tsx' : ".TO",
                   "asx" : ".AX",
                   "comex" : ".CMX",
                   "forex" : "",
                   "lse" : ".L",
                   "otcbb" : "",
                   "sgx" : ".SI",
                   "tsxv" : ".V"
                   }

    name, ext = os.path.splitext(market_file)
    name = name.lower()
    return name, suffix_dict[name]


def get_company_data_from_eodata_file(data_dir, name):
    syms = []
    nams = []
    ipos = []
    secs = []
    inds = []
    quos = []
    mark = []
    suff = []

    market, suffix = get_market_and_suffix_from_file(name)
    filename = os.path.join(data_dir, name)

    with open(filename) as f:
        lines = f.read().splitlines()
 
    count = len(lines)
    for i in range(1, count):
        s, n = lines[i].split("\t")
        syms.append(s)
        #Sanitize names
        n = n.replace("'", "")
        nams.append(n)
        ipos.append("n/a")
        secs.append("n/a")
        inds.append("n/a")
        quos.append("n/a")
        mark.append(market)
        suff.append(suffix)

    return syms, nams, ipos, secs, inds, quos, mark, suff




market_files = file_op.get_only_files(DATA_DIR)
for f in market_files:
    syms, nams, ipos, secs, inds, quos, mark, suff = get_company_data_from_eodata_file(DATA_DIR, f)
    print syms, nams, ipos, secs, inds, quos, mark, suff

    conn, cursor = db.connect_to_database("database_settings.txt")

    db.insert_companies("public.companies", cursor, syms, nams, ipos, secs, inds, quos, mark, suff)

    conn.commit()
    cursor.close()
    conn.close()

