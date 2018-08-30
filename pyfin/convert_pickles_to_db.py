from utils import file_op, db, string_op, constants, time_op
import os
import datetime
import time
from read_write import read
from argparse import ArgumentParser
import sys



def print_usage():
    print "Usage: convert_pickles_to_db.py - d yyyy-mm-dd, -c y/n"


def write_items_to_file(name, items):
    items_file = open(name, "w")
    for item in items:
        items_file.write("%s, %s, %s, %s, %s\n" % (item[0], item[1], item[2], item[3], item[4]))


parser = ArgumentParser()

parser.add_argument("-d", "--date", dest="start_date", help="Specify starting date yyyy-mm-dd")
parser.add_argument("-c", "--check_for_duplicates", dest="check_for_duplicates", help="Specify whether or not to check for duplicate record in database: y/n")

args = parser.parse_args()

param_count = len(sys.argv)

if param_count != 5:
    print_usage()
    exit()

params = vars(args)
start_with_date = params['start_date']
check_for_duplicates = params["check_for_duplicates"]

check = False
if check_for_duplicates =="y":
    check = True
elif check_for_duplicates=="n":
    check = False
else:
    print_usage()
    exit()


conn, cursor = db.connect_to_database("database/database_settings.txt")

data_dir = constants.DATA_ROOT

items = file_op.get_hierarchy_list_v2(data_dir)
write_items_to_file("items.txt", items)


items_asc = sorted(items, key=lambda t: t[3], reverse=False)
write_items_to_file("items_asc.txt", items_asc)

item_count = len(items_asc)
found = False
for  ind in range (item_count):
    if items_asc[ind][3] == start_with_date:
        found = True
        break

if not found:
    cursor.close()
    conn.close()
    exit(-1)


items_asc = items_asc[ind:]

items_to_db = time_op.group_intraday_file_records_by_dates(items_asc, 3)
db.insert_intraday_file_records_into_database(conn, cursor, items_to_db, check)


cursor.close()
conn.close()

