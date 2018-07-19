import sys
sys.path.append("../..")

import numpy as np
from utils import file_op
import os

KMEAN_LABELS_FILE = "labels_clean_kmean.txt"
CLEAN_LABELS_FILE = "labels_clean.txt"
ACCURACY_FILE = "labelling_accuracy.txt"



def load_segmentation_data(path):
    with open(path) as f:
        lines = f.read().splitlines()
        files = []
        labels = []
        probabilities = []
        clean_files = []
        clean_labels = []
        clean_probabilities = []
        for line in lines:
            id, label, prob = line.split(' : ')
            files.append(id)
            labels.append(int(label))
            probabilities.append(float(prob))
            if (float(prob) != 0.0):
                clean_files.append(id)
                clean_labels.append(int(label))
                clean_probabilities.append(float(prob))

        return files, labels, probabilities, clean_files, clean_labels, clean_probabilities,



_, _, _, clean_files, clean_labels, _ = load_segmentation_data(CLEAN_LABELS_FILE)
_, _, _, kmean_clean_files, kmean_clean_labels, _ = load_segmentation_data(KMEAN_LABELS_FILE)

out = open(ACCURACY_FILE, "w")
count = len(kmean_clean_files)

for i in range(count):
    f = kmean_clean_files[i]
    ind = clean_files.index(f)
    info = f + " : " + str(kmean_clean_labels[i]) + " : " + str(clean_labels[ind]) + "\n"
    out.write(info)


