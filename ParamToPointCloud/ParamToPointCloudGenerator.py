import numpy as np
import tensorflow as tf
from os import listdir
from os.path import isfile, join

DATA_DIR = '/raid/MyProjects/python-point-cloud/data/boxes'
BATCH_SIZE = 2
MAX_PARAM_COUNT = 8 #maximum numbe of parameters for a primitive, including label
PARAMS_VECTOR_SIZE = 256 #sparse vector for holding param values for different primitives

labels = {"box":0,
          "cylinder":1,
          "sphere":2,
          "plane":3
         }

data_files = [f for f in listdir(DATA_DIR) if isfile(join(DATA_DIR, f))]



def get_primitive_params_pos_start_from_label(label):
    label_count = len(labels)
    index = labels[label]
    pos = PARAMS_VECTOR_SIZE / label_count * int(index)
    return pos


def get_primitive_file_label_params(data_dir, name):
    params = name.split('_')
    count = len(params)
    p = np.zeros(MAX_PARAM_COUNT)

    print params



def get_point_clouds_labels_params(data_dir, files):
    arr = np.array(files)
    np.random.shuffle(arr)
    count = arr.size
    labels = np.zeros(count)
    p1 = np.zeros(count)
    p2 = np.zeros(count)
    p3 = np.zeros(count)
    p4 = np.zeros(count)
    p5 = np.zeros(count)
    for i in range(count):
        file_name = arr[i]
        get_primitive_file_label_params(data_dir, file_name)
        params = file_name.split('_')
        print params
    
    return arr


arr = get_point_clouds_labels_params(DATA_DIR, data_files)
print arr

count = arr.size 
for i in xrange(0, count, BATCH_SIZE):
    print "Batch " + str(i / BATCH_SIZE)
    print arr[i:i+BATCH_SIZE]

label_count = len(labels)
print label_count

for i in range(label_count):
    label = labels.keys()[i]
    pos = get_primitive_params_pos_start_from_label(label)
    print label
    print pos

