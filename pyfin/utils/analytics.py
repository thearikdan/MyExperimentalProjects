from scipy.spatial import distance
#import numpy as np

def get_distance(vec1, vec2):
    dist = distance.euclidean(vec1, vec2)
#    dist = np.sqrt(np.sum((vec1 - vec2) ** 2))
    return dist

