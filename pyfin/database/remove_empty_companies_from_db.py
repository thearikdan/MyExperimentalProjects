import sys
sys.path.append("..")

from utils.db import db

#The utility relies on existence of empty_record_company_ids.txt' created by find_empty_records.py
with open('empty_record_company_ids.txt', 'r') as f:
    company_ids = f.read().splitlines()

conn, cursor = db.connect_to_database("database_settings.txt")


for company_id in company_ids:
    db.delete_company_id_from_companies(conn, cursor, company_id)

cursor.close()
conn.close()

