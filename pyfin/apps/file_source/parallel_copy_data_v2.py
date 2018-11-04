import sys
sys.path.append("..")

from utils import file_op
from os.path import join, split, dirname
import os

import multiprocessing
from multiprocessing import Pool


SOURCE_DIR = '/media/ara/Passport1_2TB/pyfin/data_v2'

DEST_DIR = '/media/ara/Passport2_4TB/datasets/pyfin/data_v2' 



def get_list_of_files(source_dir):
    file_list = []
    markets = file_op.get_only_dirs(source_dir)
    for market in markets:
        market_dir = join(source_dir, market)
        symbols = file_op.get_only_dirs(market_dir)
        for symbol in symbols:
            symbol_dir = join(market_dir, symbol)
            dates = file_op.get_only_dirs(symbol_dir)
            for d in dates:
                date_dir = join(symbol_dir, d)
                times = file_op.get_only_dirs(date_dir)
                for t in times:
                    time_dir = join(date_dir, t)
                    files = file_op.get_only_files(time_dir)
                    for f in files:
                        full_path = join(time_dir, f)
                        print "Adding file: " + full_path
                        file_list.append(full_path)
    return file_list


def parallel_copy(f):
    source_len = len(SOURCE_DIR)
    symbol_path = f[source_len+1:]
    out_file = join(DEST_DIR, symbol_path)
    if not file_op.if_file_exists(out_file):
        path = dirname(out_file)

        file_op.ensure_dir_exists(path)
        print "Copying file " + f
        cmd = "cp " + f + " " + out_file 
        os.system(cmd)


file_op.ensure_dir_exists(DEST_DIR)
print "Getting the list of files..."
files = get_list_of_files(SOURCE_DIR)

print "Copying the list of files..."
p = Pool(multiprocessing.cpu_count())
p.map(parallel_copy, files)
