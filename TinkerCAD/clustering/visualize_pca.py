#http://hdbscan.readthedocs.io/en/latest/advanced_hdbscan.html
import sys
sys.path.append("../..")

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#import sklearn.datasets as data
import hdbscan
from utils import file_op
import os
from sklearn.decomposition import PCA
#%matplotlib inline

#load pointnet autoencoder data
DATA_DIR = "/raid/data/tinkercad/signatures/clean/pointnet-autoencoder"

LABELS_FILE = "labels_clean.txt"

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
        if not file_op.if_file_exists(path):
            print "Skipping file " + files[i] + " because it doesn't exist"
            continue
        data[i] = np.loadtxt(path)
    return data


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



files, labels, prob, clean_files, clean_labels, clean_probabilities = load_segmentation_data(LABELS_FILE)
count = len(files)
#count = 100

clean_data = load_signatures(DATA_DIR, clean_files)

# Number of clusters in labels, ignoring noise if present.
cluster_count = len(set(labels)) - (1 if -1 in labels else 0)
print "Number of clusters: " + str(cluster_count)

print "Noise percentage: " + str((1.0 - (float)(len(clean_files)) / len(files)) * 100.0)


#color_palette = sns.color_palette('deep', cluster_count + 1)
color_palette = sns.color_palette('bright', cluster_count + 1)
cluster_colors = [color_palette[x] if x >= 0
                  else (0.5, 0.5, 0.5)
                  for x in clean_labels]

#cluster_member_colors = [sns.desaturate(x, p) for x, p in
#                         zip(cluster_colors, prob)]
cluster_member_colors = cluster_colors

print ("Performing PCA...")
pca = PCA(2)
data_proj = pca.fit_transform(clean_data)
plt.scatter(data_proj[:,0], data_proj[:,1], s=50, linewidth=0, c=cluster_member_colors, alpha=0.25)
plt.show()
