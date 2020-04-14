import sys
sys.path.append("../..")

from utils.db import db
from etf_utils import etf_utils as eu

ROOT_DIR = "etf_data"

db_etfs = eu.get_all_dataframes_for_db(ROOT_DIR)
#print (db_etfs)
db_etfs.to_csv("dataframe.csv")

conn, cursor = db.connect_to_database("../../database/database_settings.txt")

db.insert_etf_dataframe(conn, cursor, db_etfs)

cursor.close()
conn.close()

