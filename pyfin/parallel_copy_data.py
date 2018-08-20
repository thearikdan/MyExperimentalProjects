import sys
sys.path.append("..")

from utils import file_op
from os.path import join, split, dirname
import os

import multiprocessing
from multiprocessing import Pool


SOURCE_DIR = '/media/ara/Passport1_2GB/pyfin/data_v1'

DEST_DIR = '/media/hddx/datasets/pyfin/data_v1' 



def get_list_of_files(source_dir):
    file_list = []
    symbols = file_op.get_only_dirs(source_dir)
    for symbol in symbols:
        symbol_dir = join(source_dir, symbol)
        times = file_op.get_only_dirs(symbol_dir)
        for t in times:
            time_dir = join(symbol_dir, t)
            files = file_op.get_only_files(time_dir)
            for f in files:
                full_path = join(time_dir, f)
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


print "Getting the list of files..."
files = get_list_of_files(SOURCE_DIR)

print "Copying the list of files..."
p = Pool(multiprocessing.cpu_count())
p.map(parallel_copy, files)
