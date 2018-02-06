import numpy as np
from distance import EMD

def get_equal_weights(point_count):
    weights = np.zeros((point_count))
    for i in range (point_count):
        weights[i] = 1.0 / point_count
    return weights


def get_point_cloud_1D(length, point_count):
    point_cloud = np.zeros((point_count, 3))
    for i in range (point_count):
        point_cloud[i][0] = np.random.uniform(0, length)
    return point_cloud

pc1 = get_point_cloud_1D(5, 10)
weights1 = get_equal_weights(10)
signature1 = (pc1, weights1)

pc2 = get_point_cloud_1D(8, 10)
weights2 = get_equal_weights(10)
signature2 = (pc2, weights2)

distance = EMD.getEMD(signature1, signature2)

print distance

pc3 = get_point_cloud_1D(8, 10)
weights3 = get_equal_weights(10)
signature3 = (pc3, weights3)

distance = EMD.getEMD(signature2, signature2)
print distance


