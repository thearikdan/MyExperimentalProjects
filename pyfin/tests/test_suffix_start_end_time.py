import sys
sys.path.insert(0, "../")

from utils import db

suffix, start, end = db.get_yahoo_suffix_and_trading_hours_from_symbol("../database/database_settings.txt", "AMZN")
print suffix, start, end


suffix, start, end = db.get_yahoo_suffix_and_trading_hours_from_symbol("../database/database_settings.txt", "WEED")
print suffix, start, end

