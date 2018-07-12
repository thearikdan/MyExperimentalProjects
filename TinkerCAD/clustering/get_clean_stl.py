import sys
sys.path.append("../..")

from utils import file_op
import os
from shutil import copyfile

DATA_DIR = "/raid/data/tinkercad_QuickDraw/clean_ids_from_db"

SOURCE_DIR = "/raid/data/tinkercad/stl"
DEST_DIR = "/raid/data/tinkercad/clean_stl"

NON_EXISTING_FILES = "non_existing_files.txt"
non_exist_file = open(NON_EXISTING_FILES, "w")


file_op.ensure_dir_exists(DEST_DIR)
files = file_op.get_only_files(DATA_DIR)

for f in files:
    path = os.path.join(DATA_DIR, f)
    with open(path) as f:
        lines = f.readlines()
        count = len(lines)
        for i in range(1, count):
            name = lines[i].rstrip() + ".stl"
            source_path = os.path.join(SOURCE_DIR, name)
            if file_op.if_file_exists(source_path):
                dest_path = os.path.join(DEST_DIR, name)
                copyfile(source_path, dest_path)
            else:
                non_exist_file.write(name +'\n')


