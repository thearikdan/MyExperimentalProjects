# This approach doesn't work! It takes a very long time and huge amount of memory to call the function! 
# It is better to retrieve all dates by knowing a company (AMZN) that is covered for all dates

import sys
sys.path.append("../..")

from utils.db import db


conn, cur = db.connect_to_database("../../database/database_settings.txt")


date_time_list = db.get_all_date_time_list(conn, cur)


print date_time_list

cur.close()
conn.close()



