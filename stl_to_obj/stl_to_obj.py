import sys
sys.path.append("..")

from utils import file_op
from os.path import join, splitext
import os

SOURCE_DIR = '/raid/data/tinkercad/sample2/processed'
DEST_DIR = '/raid/data/tinkercad/sample2/processed_obj'

file_op.ensure_dir_exists(DEST_DIR)
files = file_op.get_only_files(SOURCE_DIR)

for f in files:
    name, ext = splitext(f)
    in_file = join(SOURCE_DIR, f)
    out_file = join(DEST_DIR, name + ".obj")
    print "Processing file " + in_file
    cmd = "meshlabserver -i " + in_file + " -o " + out_file
    os.system(cmd)

