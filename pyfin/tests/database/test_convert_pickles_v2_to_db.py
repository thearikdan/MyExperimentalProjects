import sys
sys.path.append("../..")


from utils import file_op, db, string_op, constants, time_op
import os
import datetime
import time
from read_write import read
from argparse import ArgumentParser
import sys




def write_items_to_file(name, items):
    items_file = open(name, "w")
    for item in items:
        items_file.write("%s, %s, %s, %s, %s\n" % (item[0], item[1], item[2], item[3], item[4]))



conn, cursor = db.connect_to_database("../../database/database_settings.txt")

data_dir = "/media/hddx/datasets/pyfin/v2_test"

items = file_op.get_hierarchy_list_v2(data_dir)
write_items_to_file("items.txt", items)


items_asc = sorted(items, key=lambda t: t[3], reverse=False)
write_items_to_file("items_asc.txt", items_asc)

items_to_db = time_op.group_intraday_file_records_by_dates(items_asc, 3)
db.insert_intraday_file_records_v2_into_database(conn, cursor, items_to_db)


cursor.close()
conn.close()
