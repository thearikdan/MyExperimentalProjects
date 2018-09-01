import sys
sys.path.append("../")


from utils import db


conn, cursor = db.connect_to_database("../database/database_settings.txt")

symbol = 'AMZN'
name = db.get_exchange_name_from_symbol(conn, cursor, symbol)
if name== 'nasdaq':
    print "Nasdaq test passed"
else:
    print "Nasdaq test failed"

symbol = 'CRH'
name = db.get_exchange_name_from_symbol(conn, cursor, symbol)
if name== 'n_a':
    print "n_a test passed"
else:
    print "n_a test failed"


cursor.close()
conn.close()

