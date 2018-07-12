import sys
sys.path.append("../..")

from utils import file_op
from os.path import join, splitext
import os

from random import shuffle

import json

ROOT_DIR = "/raid/Github/MyProjects/pointnet-autoencoder-tinkercad/data/numpy_mean_0_normalized"
OUT_DIR = join(ROOT_DIR, "train_test_split")
POINTS_DIR = "points"

data_dir = join(ROOT_DIR, POINTS_DIR)
files = file_op.get_only_files(data_dir)
shuffle(files)

full_path = []
for f in files:
    path = join(data_dir, f)
    full_path.append(path)

test_file_name = join(OUT_DIR, "shuffled_test_file_list.json")

with open(test_file_name, 'w') as outfile:
    json.dump(full_path, outfile)





