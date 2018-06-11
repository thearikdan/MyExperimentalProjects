import sys
sys.path.append("..")

from utils import file_op
from os.path import join, splitext
import os

POINT_COUNT = 2048
POINT_COUNT_STR = str(POINT_COUNT)

SOURCE_DIR = '/raid/data/tinkercad/sample2/processed_obj'
DEST_DIR = '/raid/data/tinkercad/sample2/point_clouds/pcd/' + POINT_COUNT_STR

file_op.ensure_dir_exists(DEST_DIR)
files = file_op.get_only_files(SOURCE_DIR)
count = len(files)

i = 1
for f in files:
    print "Converting file " + str(i) + " out of " + str(count)
    name, ext = splitext(f)
    in_file = join(SOURCE_DIR, f)
    out_file = join(DEST_DIR, name + ".pcd")
    cmd = "pcl_mesh_sampling " + in_file + " " + out_file + " -n_samples " + POINT_COUNT_STR + " -no_vis_result"
    os.system(cmd)
    i = i + 1

