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


def get_min_with_none(l):
    count = len(l)
    count_none = 0
    m = None
    for i in range (count):
        if l[i] is None:
            count_none = count_none + 1
            continue
        if (l[i] < m) or (m is None):
            m = l[i]
    return m, float(count_none) / count
  

def get_max_with_none(l):
    count = len(l)
    count_none = 0
    m = None
    for i in range (count):
        if l[i] is None:
            count_none = count_none + 1
            continue
        if (l[i] > m) or (m is None):
            m = l[i]
    return m, float(count_none) / count


def get_avg_with_none(l):
    count = len(l)
    count_none = 0
    avg = None
    for i in range (count):
        if l[i] is None:
            count_none = count_none + 1
            continue
        elif (avg is None):
            avg = l[i]
        else:
            avg = avg + l[i]

    if avg is None:
        return avg, float(count_none) / count
    else:
        return float(avg) / (count - count_none), float(count_none) / count


def get_opening_with_none(l):
    count = len(l)
    count_none = 0
    op = None
    for i in range (count):
        if l[i] is not None:
            op = l[i]
            break

    for i in range(count):
        if l[i] is None:
            count_none = count_none + 1

    return op, float(count_none) / count


def get_closing_with_none(l):
    count = len(l)
    count_none = 0
    op = None
    for i in range (count -1 , -1, -1):
        if l[i] is not None:
            op = l[i]
            break

    for i in range(count):
        if l[i] is None:
            count_none = count_none + 1

    return op, float(count_none) / count


def get_daily_data_from_intraday_data(vl, ol, cl, hl, ll):
    min_volume, volume_none_ratio = get_min_with_none(vl)
    max_volume, _ = get_max_with_none(vl)
    avg_volume, _ = get_avg_with_none(vl)

    opening, opening_none_ratio = get_opening_with_none(ol)
    closing, closing_none_ratio = get_closing_with_none(cl)

    high, high_none_ratio = get_max_with_none(hl)
    low, low_none_ratio = get_min_with_none(ll)

    return min_volume, max_volume, avg_volume, opening, closing, high, low, volume_none_ratio, opening_none_ratio, closing_none_ratio, high_none_ratio, low_none_ratio




