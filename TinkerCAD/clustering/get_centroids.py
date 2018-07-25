import sys
sys.path.append("../..")

from utils import file_op
import os
import numpy as np

POINT_COUNT = 2048
DIM = 3

CLEAN_IDS_FRON_DB = "/raid/data/tinkercad_QuickDraw/clean_ids_from_db"
DATA_DIR = "/raid/data/tinkercad/point_clouds/clean_numpy/2048/numpy_mean_0_normalized_clean"
OUT_DIR = "/raid/data/tinkercad/point_clouds/clean_numpy/2048/centroids"


files = file_op.get_only_files(CLEAN_IDS_FRON_DB)
count = len(files)

for f in files:
    class_name, _ = os.path.splitext(f)
    path = os.path.join(CLEAN_IDS_FRON_DB, f)
    with open(path) as f:
        lines = f.readlines()
        count = len(lines)
        val = np.zeros((POINT_COUNT, DIM))
        file_name = class_name + ".txt"
        file_name = os.path.join(OUT_DIR, file_name)
        for i in range(1, count):
            name = lines[i].rstrip() + ".txt"
            name = os.path.join(DATA_DIR, name)
            if not file_op.if_file_exists(name):
                continue
            val = val + np.loadtxt(name)
        val = val / count
        np.savetxt(file_name, val)


