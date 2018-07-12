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

size = len(full_path)
train_size = int(0.8 * size)

rest_size = size - train_size
test_size = int (0.5 * rest_size)
val_size = rest_size - test_size

train_data = full_path[:train_size]
test_data = full_path[train_size:(train_size + test_size)]
val_data = full_path[(train_size + test_size):]

train_file_name = join(OUT_DIR, "shuffled_train_file_list.json")
test_file_name = join(OUT_DIR, "shuffled_test_file_list.json")
val_file_name = join(OUT_DIR, "shuffled_val_file_list.json")

with open(train_file_name, 'w') as outfile:
    json.dump(train_data, outfile)

with open(test_file_name, 'w') as outfile:
    json.dump(test_data, outfile)

with open(val_file_name, 'w') as outfile:
    json.dump(val_data, outfile)




