from scipy.spatial import distance
import numpy as np
import math



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


def get_min_with_nan(l):
    count = len(l)
    count_nan = 0
    m = float('nan')
    for i in range (count):
        if math.isnan(l[i]):
            count_nan = count_nan + 1
            continue
        if (l[i] < m) or (math.isnan(m)):
            m = l[i]
    return m, float(count_nan) / count
  

def get_max_with_nan(l):
    count = len(l)
    count_nan = 0
    m = float('nan')
    for i in range (count):
        if math.isnan(l[i]):
            count_nan = count_nan + 1
            continue
        if (l[i] > m) or (math.isnan(m)):
            m = l[i]
    return m, float(count_nan) / count


def get_avg_with_nan(l):
    count = len(l)
    count_nan = 0
    avg = float('nan')
    for i in range (count):
        if math.isnan(l[i]):
            count_nan = count_nan + 1
            continue
        elif (math.isnan(avg)):
            avg = l[i]
        else:
            avg = avg + l[i]

    if math.isnan(avg):
        return avg, float(count_none) / count
    else:
        return float(avg) / (count - count_nan), float(count_nan) / count


def get_opening_with_nan(l):
    count = len(l)
    count_nan= 0
    op = float('nan')
    for i in range (count):
        if not math.isnan(l[i]):
            op = l[i]
            break

    for i in range(count):
        if math.isnan(l[i]):
            count_nan = count_nan + 1

    return op, float(count_nan) / count


def get_closing_with_nan(l):
    count = len(l)
    count_nan = 0
    op = None
    for i in range (count -1 , -1, -1):
        if not math.isnan(l[i]):
            op = l[i]
            break

    for i in range(count):
        if math.isnan(l[i]):
            count_nan = count_nan + 1

    return op, float(count_nan) / count


def get_daily_data_from_intraday_data(vl, ol, cl, hl, ll):
    min_volume, volume_none_ratio = get_min_with_nan(vl)
    max_volume, _ = get_max_with_nan(vl)
    avg_volume, _ = get_avg_with_nan(vl)

    opening, opening_nan_ratio = get_opening_with_nan(ol)
    closing, closing_nan_ratio = get_closing_with_nan(cl)

    high, high_nan_ratio = get_max_with_nan(hl)
    low, low_nan_ratio = get_min_with_nan(ll)

    return min_volume, max_volume, avg_volume, opening, closing, high, low, volume_none_ratio, opening_nan_ratio, closing_nan_ratio, high_nan_ratio, low_nan_ratio




