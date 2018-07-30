import sys
sys.path.append("..")

from utils import file_op, db
import psycopg2
import os

DATA_DIR = "../downloads/misc"


def get_company_data_from_misc_file(data_dir, name):
    syms = []
    nams = []
    ipos = []
    secs = []
    inds = []
    quos = []
    mark = []
    suff = []

    filename = os.path.join(data_dir, name)

    with open(filename) as f:
        lines = f.read().splitlines()
 
    count = len(lines)
    for i in range(count):
        s = lines[i]
        syms.append(s)
        #Sanitize names
        n = ("n/a")
        nams.append(n)
        ipos.append("n/a")
        secs.append("n/a")
        inds.append("n/a")
        quos.append("n/a")
        mark.append("n/a")
        suff.append("")

    return syms, nams, ipos, secs, inds, quos, mark, suff




market_files = file_op.get_only_files(DATA_DIR)
for f in market_files:
    syms, nams, ipos, secs, inds, quos, mark, suff = get_company_data_from_misc_file(DATA_DIR, f)
#    print syms, nams, ipos, secs, inds, quos, mark, suff

    conn, cursor = db.connect_to_database("database_settings.txt")

    db.insert_companies("public.companies", cursor, syms, nams, ipos, secs, inds, quos, mark, suff)

    conn.commit()
    cursor.close()
    conn.close()

