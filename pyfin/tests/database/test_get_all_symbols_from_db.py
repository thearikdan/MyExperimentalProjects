import sys
sys.path.insert(0, "../..")

from utils import db

symbols = db.get_all_symbols("../database/database_settings.txt")
print symbols
