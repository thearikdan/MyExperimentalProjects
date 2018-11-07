import sys
sys.path.append("../..")


from utils import file_op, string_op, constants, time_op
import os
import datetime
import time
from utils.file_system import read
from utils.db import db
import sys




def write_items_to_file(name, items):
    items_file = open(name, "w")
    for item in items:
        items_file.write("%s, %s, %s, %s, %s\n" % (item[0], item[1], item[2], item[3], item[4]))


script_start_time = time.time()


conn, cursor = db.connect_to_database("../../database/database_settings.txt")

start_date = "2018-11-5"


data_dir = "/media/hddx/datasets/pyfin/data"

items = file_op.get_hierarchy_list_v2(data_dir)
write_items_to_file("items.txt", items)


items_asc = sorted(items, key=lambda t: t[3], reverse=False)
write_items_to_file("items_asc.txt", items_asc)


start_date_time = time_op.convert_date_to_datetime(start_date)

item_count = len(items_asc)
found = False
for  ind in range (item_count):
    if items_asc[ind][3] == start_date_time:
        found = True
        break

if not found:
    cursor.close()
    conn.close()
    exit(-1)

items_asc = items_asc[ind:]

records = time_op.group_intraday_file_records_by_dates(items_asc, 3)

db.insert_intraday_file_records_v2_into_database(conn, cursor, records)


cursor.close()
conn.close()


seconds = time.time() - script_start_time

mint, s = divmod(seconds, 60)
h, m = divmod(mint, 60)

print "Elapsed time: %d hours :%02d minutes :%02d seconds" % (h, m, s)

