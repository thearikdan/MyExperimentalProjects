import sys
sys.path.append("../")


from utils import db


conn, cursor = db.connect_to_database("../database/database_settings.txt")

symbol = 'AMZN'
name = db.get_data_v1_exchange_name_from_symbol(conn, cursor, symbol)
print name

symbol = 'CRH'
name = db.get_data_v1_exchange_name_from_symbol(conn, cursor, symbol)
print name

cursor.close()
conn.close()

