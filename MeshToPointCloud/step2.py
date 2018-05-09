import sys
sys.path.append("..")

from utils import file_op
from os.path import join, splitext
import os
import random

SOURCE_DIR = '/raid/data/tinkercad/sample2/test_pc/step_1'
DEST_DIR = '/raid/data/tinkercad/sample2/test_pc/step_2'
 
dest_point_count = 1024

file_op.ensure_dir_exists(DEST_DIR)
files = file_op.get_only_files(SOURCE_DIR)

for f in files:
    in_file = join(SOURCE_DIR, f)
    points_file = open(in_file, 'r')
    lines = points_file.readlines()
    count = len(lines)
    if (dest_point_count > count):
        continue
    indices = sorted(random.sample(range(count), dest_point_count))
    out_file = join(DEST_DIR, f)
    step2_file = open(out_file, 'w')
    for i in range(dest_point_count):
        step2_file.write(lines[indices[i]])

