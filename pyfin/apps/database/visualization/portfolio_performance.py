import sys
sys.path.append("../../..")
from utils.db import db


YAHOO_PORTFOLIO_EXPORTED_FILE = "quotes.csv"
target_exchanges = ['nyse', 'nasdaq', 'otcbb']
conn, cursor = db.connect_to_database("../../../database/database_settings.txt")

symbols, exchanges = db.get_symbols_and_exchanges_from_yahoo_csv(conn, cursor, YAHOO_PORTFOLIO_EXPORTED_FILE, target_exchanges)

print symbols
print exchanges

cursor.close()
conn.close()


