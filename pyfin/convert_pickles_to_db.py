from utils import file_op, db, string_op
import os
import datetime
import time
from read_write import read



DATA_DIR = "data_v2"

#find index of start day
start_with_day = '2018-8-6'


def get_filename_from_item(item):
    filename = os.path.join(item[0], item[1])
    filename = os.path.join(filename, item[2])
    filename = os.path.join(filename, item[3])
    filename = os.path.join(filename, item[4])
    filename = os.path.join(filename, item[5])
    return filename


def insert_items_into_database(conn, cur, item_to_db):
    count = len(item_to_db)
    for i in range(count):
        item_count = len(item_to_db[i])
        for j in range (item_count):
            item = item_to_db[i][j]
            filename = get_filename_from_item(item)
            date_time, volume, opn, close, high, low = read.get_all_intraday_data_from_file(filename)
            suffix_list = db.get_suffix_list(conn, cur)
            market = item[1]
            symbol = string_op.get_symbol_without_suffix(item[2], suffix_list)
            suffix = string_op.get_suffix_without_symbol(item[2], suffix_list)
            if read.is_price_list_corrupt(close):
                db.add_to_corrupt_intraday_prices(conn, cur, market, symbol, item[3])
            else:
                db.add_to_intraday_prices(conn, cur, market, symbol, date_time, volume, opn, close, high, low)
        conn.commit()


def write_items_to_file(name, items):
    items_file = open(name, "w")
    for item in items:
        items_file.write("%s, %s, %s, %s, %s\n" % (item[0], item[1], item[2], item[3], item[4]))


def get_dates_list(items):
    dates = []
    dates.append(items[0][3])

    for item in items:
        count = len(dates)
        if item[3] != dates[count - 1]:
            dates.append(item[3])
    return dates


def convert_date_to_datetime(date):
    year, month, day = date.split("-")
    return datetime.date(int(year), int(month), int(day))


def group_items_by_dates(items):
    dates = get_dates_list(items)
    dates_count = len(dates)

    items_to_db = []
    for i in range(dates_count):
        items_to_db.append([])

    for item in items_asc:
        for i in range(dates_count):
            if item[3] == dates[i]:
                items_to_db[i].append(item)

    return items_to_db


def get_hierarchy_list(data_dir):
    items = []

    markets = file_op.get_only_dirs(data_dir)
    for market in markets:
        market_dir = os.path.join(DATA_DIR, market)
        tickers = file_op.get_only_dirs(market_dir)
        ticker_count = len(tickers)

        for i in range (ticker_count):
#    for i in range(10):
            sub_dir = os.path.join(market_dir, tickers[i])
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
                        item = (DATA_DIR, market, tickers[i], dates[j], intervals[k], files[l])
#                        print item
                        items.append((item))
    return items



conn, cursor = db.connect_to_database("database/database_settings.txt")

start_time = time.clock()
print ("Getting hierarchy of files")

print ("Starting time:")
print(datetime.datetime.now())

items = get_hierarchy_list(DATA_DIR)
write_items_to_file("items.txt", items)

print ("Got hierarchy at time:")
print(datetime.datetime.now())

print "Item count: " + str(len(items))

start_time = time.clock()
print "Sorting by ascending" 

items_asc = sorted(items, key=lambda t: t[3], reverse=False)
write_items_to_file("items_asc.txt", items_asc)

item_count = len(items_asc)
found = False
for  ind in range (item_count):
    if items_asc[ind][3] == start_with_day:
        found = True
        break

if not found:
    cursor.close()
    conn.close()
    exit(-1)


items_asc = items_asc[ind:]

items_to_db = group_items_by_dates(items_asc)
insert_items_into_database(conn, cursor, items_to_db)

print ("Ending time:")
print(datetime.datetime.now())


cursor.close()
conn.close()

