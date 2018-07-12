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
DATA_DIR = "/raid/data/tinkercad/signatures/pointnet-autoencoder"

LABELS_FILE = "labels.txt"

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


def load_segmentation_data(path):
    with open(path) as f:
        lines = f.read().splitlines()
        files = []
        labels = []
        probabilities = []
        for line in lines:
            id, label, prob = line.split(' : ')
            files.append(id)
            labels.append(int(label))
            probabilities.append(float(prob))
        return files, labels, probabilities



files, labels, prob = load_segmentation_data("labels_clean.txt")
count = len(files)
#count = 100

data = load_signatures(DATA_DIR, files)

# Number of clusters in labels, ignoring noise if present.
cluster_count = len(set(labels)) - (1 if -1 in labels else 0)
print "Number of clusters: " + str(cluster_count)


color_palette = sns.color_palette('deep', cluster_count + 1)
cluster_colors = [color_palette[x] if x >= 0
                  else (0.5, 0.5, 0.5)
                  for x in labels]

cluster_member_colors = [sns.desaturate(x, p) for x, p in
                         zip(cluster_colors, prob)]
#cluster_member_colors = cluster_colors

print ("Performing PCA...")
pca = PCA(2)
data_proj = pca.fit_transform(data)
plt.scatter(data_proj[:,0], data_proj[:,1], s=50, linewidth=0, c=cluster_member_colors, alpha=0.25)
plt.show()
