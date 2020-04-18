import sys
sys.path.append("../..")

from utils.db import db

conn, cur = db.connect_to_database("../../database/database_settings.txt")

company_ids = db.get_all_company_ids(conn, cur)
print(company_ids)
print (len(company_ids))
print("-------------------------------------------")

etf_ids = db.get_all_etf_ids(conn, cur)
print(etf_ids)
print (len(etf_ids))

cur.close()
conn.close()


