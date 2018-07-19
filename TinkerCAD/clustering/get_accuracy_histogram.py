import sys
sys.path.append("../..")

import numpy as np
from utils import file_op
import os
import matplotlib.pyplot as plt


ACCURACY_FILE = "labelling_accuracy.txt"


def load_accuracy_data(path):
    with open(path) as f:
        lines = f.read().splitlines()
        files = []
        kmean_labels = []
        clean_labels = []
        for line in lines:
            f, k, c = line.split(' : ')
            files.append(f)
            kmean_labels.append(int(k))
            clean_labels.append(int(c))

        return files, kmean_labels, clean_labels


files, kmean_labels, clean_labels = load_accuracy_data(ACCURACY_FILE)

kmean_set = set(kmean_labels)
print kmean_set

count = len(files)

histogramme = []
for k in kmean_set:
    clean = []
    for i in range(count):
        if ((kmean_labels[i]) == k):
            clean.append(clean_labels[i])
    histogramme.append(clean)

f, (ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9) = plt.subplots(9, sharex=True, sharey=True)


ax1.hist(histogramme[0])
ax2.hist(histogramme[1])
ax3.hist(histogramme[2])
ax4.hist(histogramme[3])
ax5.hist(histogramme[4])
ax6.hist(histogramme[5])
ax7.hist(histogramme[6])
ax8.hist(histogramme[7])
ax9.hist(histogramme[8])

#plt.hist(histogramme[8])

plt.show()