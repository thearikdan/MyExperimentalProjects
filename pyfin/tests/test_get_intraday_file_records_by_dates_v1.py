import sys
sys.path.append("../")

from utils import file_op, time_op
import os
import datetime
import time
from read_write import read
import sys


def write_items_to_file(name, items):
    items_file = open(name, "w")
    for item in items:
        items_file.write("%s, %s, %s, %s, %s\n" % (item[0], item[1], item[2], item[3], item[4]))


data_dir = "/media/hddx/datasets/pyfin/v1_test"

items = file_op.get_hierarchy_list_v1(data_dir)
write_items_to_file("items.txt", items)


items_asc = sorted(items, key=lambda t: t[2], reverse=False)
write_items_to_file("items_asc.txt", items_asc)

records = time_op.group_intraday_file_records_by_dates(items_asc, 2)
print records



