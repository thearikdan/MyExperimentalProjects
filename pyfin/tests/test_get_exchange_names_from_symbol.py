import sys
sys.path.append("../")


from utils import db


conn, cursor = db.connect_to_database("../database/database_settings.txt")

symbol = 'AMZN'
names = db.get_exchange_names_from_symbol(conn, cursor, symbol)
print names

symbol = 'CRH'
names = db.get_exchange_names_from_symbol(conn, cursor, symbol)
print names

cursor.close()
conn.close()

