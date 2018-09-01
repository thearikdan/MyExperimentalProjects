import sys
sys.path.append("../")


from utils import db


conn, cursor = db.connect_to_database("../database/database_settings.txt")

symbol = 'AMZN'
ids = db.get_exchange_ids_from_symbol(conn, cursor, symbol)
print ids

symbol = 'CRH'
ids = db.get_exchange_ids_from_symbol(conn, cursor, symbol)
print ids

cursor.close()
conn.close()

