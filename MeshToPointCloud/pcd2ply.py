import sys
sys.path.append("..")

from utils import file_op
from os.path import join, splitext
import os

import multiprocessing
from multiprocessing import Pool


POINT_COUNT = 2048
POINT_COUNT_STR = str(POINT_COUNT)

SOURCE_DIR = '/raid/data/tinkercad/sample2/point_clouds/pcd/' + POINT_COUNT_STR
DEST_DIR = '/raid/data/tinkercad/sample2/point_clouds/ply/' + POINT_COUNT_STR + '/ascii/'

def convert(f):
    name, ext = splitext(f)
    in_file = join(SOURCE_DIR, f)
    out_file = join(DEST_DIR, name + ".ply")
    cmd = "pcl_pcd2ply -format 0 " + in_file + " " + out_file #ascii
#    cmd = "pcl_pcd2ply -format 1 " + in_file + " " + out_file #binary
    os.system(cmd)

file_op.ensure_dir_exists(DEST_DIR)
files = file_op.get_only_files(SOURCE_DIR)

p = Pool(multiprocessing.cpu_count())
p.map(convert, files)
