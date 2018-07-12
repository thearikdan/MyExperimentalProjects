import sys
sys.path.append("../..")

from utils import file_op
import os

DATA_DIR = "/raid/data/tinkercad_QuickDraw/clean_ids_from_db"

LABELS_FILE = "labels_clean.txt"


files = file_op.get_only_files(DATA_DIR)
count = len(files)


label = 1

out_file = open(LABELS_FILE, "w")

for f in files:
    path = os.path.join(DATA_DIR, f)
    with open(path) as f:
        lines = f.readlines()
        count = len(lines)
        for i in range(1, count):
            rec = lines[i].rstrip() + ".txt" + " : " + str(label) + " : " + "1.0\n"
            out_file.write(rec)
    label = label + 1


