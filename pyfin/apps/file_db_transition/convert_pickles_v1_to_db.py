from utils import file_op, time_op, db
import os
import datetime
import time
from utils.read_write import read
import sys


def write_items_to_file(name, items):
    items_file = open(name, "w")
    for item in items:
        items_file.write("%s, %s, %s, %s, %s\n" % (item[0], item[1], item[2], item[3], item[4]))

conn, cursor = db.connect_to_database("../database/database_settings.txt")

start_date = "2018-4-18                                                                                   "

data_dir = "/media/hddx/datasets/pyfin/data_v1"

items = file_op.get_hierarchy_list_v1(data_dir)
write_items_to_file("items.txt", items)


items_asc = sorted(items, key=lambda t: t[2], reverse=False)
write_items_to_file("items_asc.txt", items_asc)


start_date_time = time_op.convert_date_to_datetime(start_date)

item_count = len(items_asc)
found = False
for  ind in range (item_count):
    if items_asc[ind][2] == start_date_time:
        found = True
        break

if not found:
    cursor.close()
    conn.close()
    exit(-1)


items_asc = items_asc[ind:]


records = time_op.group_intraday_file_records_by_dates(items_asc, 2)

db.insert_intraday_file_records_v1_into_database(conn, cursor, records)


cursor.close()
conn.close()

