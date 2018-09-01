import sys
sys.path.append("../")


from utils import db


conn, cursor = db.connect_to_database("../database/database_settings.txt")

symbol = 'AMZN'
id = db.get_exchange_id_from_symbol(conn, cursor, symbol)
if id==1:
    print "Nasdaq test passed"
else:
    print "Nasdaq test failed"

symbol = 'CRH'
id = db.get_exchange_id_from_symbol(conn, cursor, symbol)
if id==10:
    print "n_a test passed"
else:
    print "n_a test failed"

cursor.close()
conn.close()

