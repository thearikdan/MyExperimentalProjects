import sys
sys.path.append("../..")

from utils.db import db
from etf_utils import etf_utils as eu

ROOT_DIR = "etf_data"

categories = eu.get_all_categories(ROOT_DIR)

conn, cursor = db.connect_to_database("../../database/database_settings.txt")

db.insert_etf_categories(conn, cursor, categories)

cursor.close()
conn.close()