import sys
sys.path.append("..")

from utils.db import db

conn, cursor = db.connect_to_database("database_settings.txt")

empty_company_ids = []

all_company_ids = db.get_all_company_ids(conn, cursor)

for company_id in all_company_ids:
    print ("Checking company id " + str(company_id))
    exists = db.if_record_exists_in_intraday_prices_for_company_id(conn, cursor, company_id)
    if not exists:
        print("Adding to empty record list!")
        empty_company_ids.append(company_id)

cursor.close()
conn.close()

with open('empty_record_company_ids.txt', 'w') as f:
    for id in empty_company_ids:
        f.write("%s\n" % id)
