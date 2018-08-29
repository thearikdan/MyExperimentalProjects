import sys
sys.path.append("../")

from utils import file_op, string_op, constants
import os
import datetime
import time
from read_write import read
import sys


def write_items_to_file(name, items):
    items_file = open(name, "w")
    for item in items:
        items_file.write("%s, %s, %s, %s, %s\n" % (item[0], item[1], item[2], item[3], item[4]))


data_dir = "/media/hddx/datasets/pyfin/v2_test"

items = file_op.get_hierarchy_list_v2(data_dir)
write_items_to_file("items.txt", items)


items_asc = sorted(items, key=lambda t: t[3], reverse=False)
write_items_to_file("items_asc.txt", items_asc)



