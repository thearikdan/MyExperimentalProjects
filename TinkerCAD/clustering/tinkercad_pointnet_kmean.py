#http://hdbscan.readthedocs.io/en/latest/advanced_hdbscan.html
import sys
sys.path.append("../..")

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from utils import file_op
import os

#load pointnet autoencoder data
DATA_DIR = "/raid/data/tinkercad/signatures/clean/pointnet-autoencoder"

LABELS_FILE = "labels_clean_kmean.txt"

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

print ("Performing K-MEAN...")
clusterer = KMeans(n_clusters=9) #9 clean classes so far
clusterer.fit(data)

print ("Saving labels...")
labels = clusterer.labels_
probabilities = np.ones(count) #no probabilities for k-mean, assigning to 1 to compy with the rest
label_file = open(LABELS_FILE, "w")
for i in range(count):
    s = files[i] + " : " + str(int(labels[i])) + " : " + str(probabilities[i]) + '\n'
    label_file.write(s)

label_file.close()


