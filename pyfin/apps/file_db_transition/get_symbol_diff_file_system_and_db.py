from utils import file_op
from utils import db


def write_items_to_file(name, items):
    items_file = open(name, "w")
    for item in items:
        items_file.write("%s\n" % item)


def write_in_l1_not_l2(filename, l1, l2):
    in_l1_not_l2 = []
    for l in l1:
        if l not in l2:
            in_l1_not_l2.append(l)
    write_items_to_file(filename, in_l1_not_l2)


file_symbols = file_op.get_all_symbols("data")
db_symbols = db.get_all_symbols("database/database_settings.txt")


write_in_l1_not_l2("in_file_system_not_in_database.txt", file_symbols, db_symbols)
write_in_l1_not_l2("in_database_not_in_file_system.txt", db_symbols, file_symbols)


