#http://hdbscan.readthedocs.io/en/latest/advanced_hdbscan.html
import sys
sys.path.append("../..")

import numpy as np
import matplotlib.pyplot as plt
import hdbscan
from utils import file_op
import os
#%matplotlib inline

#load pointnet autoencoder data
DATA_DIR = "/raid/data/tinkercad/signatures/pointnet-autoencoder"

LABELS_FILE = "labels_min_25.txt"

def load_signatures(data_dir, files):
    count = len(files)
#    count = 100
    path0 = os.path.join(data_dir, files[0])
    sig0 = np.loadtxt(path0)
    sig_shape = sig0.shape
    data = np.zeros((count, sig_shape[0]))
    for i in range(count):
        print "Loading file " + files[i] + " :" + str(i) + " out of " + str(count)
        path = os.path.join(data_dir, files[i])
        data[i] = np.loadtxt(path)
    return data


files = file_op.get_only_files(DATA_DIR)
count = len(files)
#count = 100

data = load_signatures(DATA_DIR, files)

print ("Performing HDBSCAN...")
clusterer = hdbscan.HDBSCAN(min_cluster_size=25, gen_min_span_tree=True)
clusterer.fit(data)

print ("Saving labels...")
labels = clusterer.labels_
probabilities = clusterer.probabilities_
label_file = open(LABELS_FILE, "w")
for i in range(count):
    s = files[i] + " : " + str(int(labels[i])) + " : " + str(probabilities[i]) + '\n'
    label_file.write(s)

label_file.close()

# Number of clusters in labels, ignoring noise if present.
cluster_count = len(set(labels)) - (1 if -1 in labels else 0)
print "Number of clusters: " + str(cluster_count)


