from scipy.spatial import distance
import numpy as np



def get_distance(vec1, vec2):
    dist = distance.euclidean(vec1, vec2)
#    dist = np.sqrt(np.sum((vec1 - vec2) ** 2))
    return dist


def get_distance_list(reference, my_list):
    dist_list = []
    count = len(my_list)
    for i in range (count):
        vec1 = np.array(reference)
        vec2 = np.array(my_list[i])
        dist = get_distance(vec1, vec2)
        dist_list.append(dist)

    return dist_list



