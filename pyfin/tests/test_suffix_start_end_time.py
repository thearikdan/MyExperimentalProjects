import sys
sys.path.insert(0, "../")

from utils import db

conn, cursor = db.connect_to_database("../database/database_settings.txt")

suffix, start, end = db.get_yahoo_suffix_and_trading_hours_from_symbol(conn, cursor, "AMZN")
print suffix, start, end


suffix, start, end = db.get_yahoo_suffix_and_trading_hours_from_symbol(conn, cursor, "WEED")
print suffix, start, end

