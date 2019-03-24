import sys
sys.path.append("../../..")

from utils.db import db


conn, cur = db.connect_to_database("../../../database/database_settings.txt")


symbols, markets = db.get_all_symbols_and_markets(conn, cur)


print (symbols, markets)
print len(symbols)
print len(markets)

cur.close()
conn.close()



