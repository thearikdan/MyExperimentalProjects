from scipy.spatial import distance

def get_distance(vec1, vec2):
    dist = distance.euclidean(vec1, vec2)
    return dist

