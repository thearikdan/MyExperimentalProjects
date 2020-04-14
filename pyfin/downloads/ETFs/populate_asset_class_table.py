import sys
sys.path.append("../..")

from utils.db import db
from etf_utils import etf_utils as eu

ROOT_DIR = "etf_data"

asset_classes = eu.get_all_asset_classes(ROOT_DIR)

conn, cursor = db.connect_to_database("../../database/database_settings.txt")

db.insert_etf_asset_classes(conn, cursor, asset_classes)

cursor.close()
conn.close()

print(asset_classes)

