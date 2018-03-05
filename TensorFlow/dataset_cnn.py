import os
from glob import glob
from os.path import dirname

TRAIN_DIR = "/raid/data/cnn/m40/train"
TEST_DIR = "/raid/data/cnn/m40/test" 

def get_labels_from_files(files):
    labels = []
    for f in files:
        directory = dirname(f)
        dirs = directory.split('/')
        dirs_len = len(dirs)
        labels.append(dirs[dirs_len - 1])
    return labels


def convert_labels_to_numbers(labels, classes):
    label_numbers = []
    label_count = len(labels)
    class_count = len(classes)
    for i in range (label_count):
        for j in range (class_count):
            if labels[i] == classes[j]:
                label_numbers.append(j)
    return label_numbers



train_files = [y for x in os.walk(TRAIN_DIR) for y in glob(os.path.join(x[0], '*.png'))]
train_labels = get_labels_from_files(train_files)
classes = list(set(train_labels))
train_classes = convert_labels_to_numbers(train_labels, classes)

test_files = [y for x in os.walk(TEST_DIR) for y in glob(os.path.join(x[0], '*.png'))]
test_labels = get_labels_from_files(test_files)
test_classes = convert_labels_to_numbers(test_labels, classes)
