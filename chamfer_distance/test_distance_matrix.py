import numpy as np
from distance import utils, nndistance_cpu

a = np.array([[[[0, 2], [0, 4]]], [[[0, 2], [0, 4]]], [[[2, 0], [4, 0]]], [[[2, 0], [4, 0]]], [[[2, 2], [4, 4]]], [[[2, 2], [4, 4]]]])


s = a.shape
b = np.zeros(s)

print s

pc_count = a.shape[0]
batch_size = a.shape[1]
dist = np.zeros((pc_count, pc_count))


for i in range (pc_count):
    for j in range(batch_size):
        a_norm = utils.pc_normalize(a[i][j])
        b[i][j] = a_norm

#print b

for i in range(pc_count):
    for j in range (i, pc_count):
        dist[i, j] = nndistance_cpu.nn_distance_cpu(b[i], b[j])
        dist [j, i] = dist[i, j]
 
#print b
print dist
