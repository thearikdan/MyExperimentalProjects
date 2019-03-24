import sys
sys.path.append("../../..")

from utils.db import db

market = 'nasdaq'
symbol = 'AMZN'

conn, cur = db.connect_to_database("../../../database/database_settings.txt")


date_time_list = db.get_all_year_month_day_list_for_symbol(conn, cur, market, symbol)


print (date_time_list)
print len(date_time_list)

cur.close()
conn.close()



