from utils import file_op, db, string_op
import os
import datetime
import time
from read_write import read



DATA_DIR = "data"

def get_filename_from_item(item):
    filename = os.path.join(item[0], item[1])
    filename = os.path.join(filename, item[2])
    filename = os.path.join(filename, item[3])
    filename = os.path.join(filename, item[4])
    return filename


def insert_item_into_database(conn, cur, item):
    filename = get_filename_from_item(item)
    date_time, volume, opn, close, high, low = read.get_all_intraday_data_from_file(filename)
    suffix_list = db.get_suffix_list("database/database_settings.txt")
    symbol = string_op.get_symbol_without_suffix(item[1], suffix_list)
    suffix = string_op.get_suffix_without_symbol(item[1], suffix_list)
    if read.is_price_list_corrupt(close):
        db.add_to_corrupt_intraday_prices(conn, cur, symbol, suffix, item[2])
    else:
        return;


def write_items_to_file(name, items):
    items_file = open(name, "w")
    for item in items:
        items_file.write("%s, %s, %s, %s, %s\n" % (item[0], item[1], item[2], item[3], item[4]))


def convert_date_to_datetime(date):
    year, month, day = date.split("-")
    return datetime.date(int(year), int(month), int(day))

def get_hierarchy_list(data_dir):
    items = []

    tickers = file_op.get_only_dirs(data_dir)
    ticker_count = len(tickers)

    for i in range (ticker_count):
        sub_dir = os.path.join(DATA_DIR, tickers[i])
        dates = file_op.get_only_dirs(sub_dir)
        date_count = len(dates)
        for j in range(date_count):
            sub_sub_dir = os.path.join(sub_dir, dates[j])
            intervals = file_op.get_only_dirs(sub_sub_dir)
            interval_count = len(intervals)
            for k in range(interval_count):
                sub_sub_sub_dir= os.path.join(sub_sub_dir, intervals[k])
                files = file_op.get_only_files(sub_sub_sub_dir)
                file_count = len(files)
                for l in range(file_count):
                    item = (DATA_DIR, tickers[i], dates[j], intervals[k], files[l])
#                    print item
                    items.append((item)) 
    return items


conn, cursor = db.connect_to_database("database/database_settings.txt")

start_time = time.clock()
print ("Getting hierarchy of files")

print ("Starting time:")
print(datetime.datetime.now())

items = get_hierarchy_list(DATA_DIR)

seconds = time.clock() - start_time

m, s = divmod(seconds, 60)
h, m = divmod(m, 60)
#print "Elapsed time to get hierarchy: %d hours :%02d minutes :%02d seconds" % (h, m, s)

#write_items_to_file("items.txt", items)

print ("Got hierarchy at time:")
print(datetime.datetime.now())

start_time = time.clock()
print "Sorting by ascending" 

items_asc = sorted(items, key=lambda t: t[2], reverse=False)
print items_asc

for item in items_asc:
    insert_item_into_database(conn, cursor, item)

seconds = time.clock() - start_time

m, s = divmod(seconds, 60)
h, m = divmod(m, 60)
#print "Elapsed time to get sort: %d hours :%02d minutes :%02d seconds" % (h, m, s)
print "Record count: %d" % len(items_asc)

write_items_to_file("items_asc.txt", items_asc)

print ("Ending time:")
print(datetime.datetime.now())

conn.commit()
cursor.close()
conn.close()

