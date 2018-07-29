from utils import file_op
import os
import datetime
import time

DATA_DIR = "data"


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
#                    item = (DATA_DIR, tickers[i], convert_date_to_datetime(dates[j]), intervals[k], files[l])
                    item = (DATA_DIR, tickers[i], dates[j], intervals[k], files[l])
#                    print item
                    items.append((item)) 
    return items

start_time = time.clock()
print ("Getting hierarchy of files")
items = get_hierarchy_list(DATA_DIR)

seconds = time.clock() - start_time

m, s = divmod(seconds, 60)
h, m = divmod(m, 60)
print "Elapsed time to get hierarchy: %d hours :%02d minutes :%02d seconds" % (h, m, s)

write_items_to_file("items.txt", items)


start_time = time.clock()
print "Sorting by ascending" 

items_asc = sorted(items, key=lambda t: t[2], reverse=False)
print items_asc

seconds = time.clock() - start_time

m, s = divmod(seconds, 60)
h, m = divmod(m, 60)
print "Elapsed time to get sort: %d hours :%02d minutes :%02d seconds" % (h, m, s)
print "Record count: %d" % len(items_asc)

write_items_to_file("items_asc.txt", items_asc)


