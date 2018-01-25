import numpy as np


def interpolate_by_distance(my_list, dist, interp_count):
    list_count = len(my_list)
    if (list_count == 0):
        return []
    dist_count = len(dist)
    if (list_count != dist_count):
        raise Exception('Distances and lists must have the same length!')

    if (interp_count > list_count):
        interp_count = list_count

    weights = []
    for i in range (interp_count):
        if (dist[i] == 0):
            #exact match, no need to interpolate
            interp = my_list[i]
            return interp
        else:
            weight = 1 / dist[i]
            weights.append(weight)

    weight_sum = sum(weights)
    
    weights_np = np.array(weights) / weight_sum

    interp = []
    dim = len(my_list[0])
    my_np = np.zeros(dim)
    for i in range (interp_count):
        list_np = np.array(my_list[i])
        list_np = list_np * weights_np[i]
        my_np += list_np

    interp = my_np.tolist()
    return interp



def interpolate_prices_and_volume_by_distance(volume_per_list, open_per_list, close_per_list, high_per_list, low_per_list, dist, interp_count):
    interp_volume_per = interpolate_by_distance(volume_per_list, dist, interp_count)
    interp_open_per = interpolate_by_distance(open_per_list, dist, interp_count)
    interp_close_per = interpolate_by_distance(close_per_list, dist, interp_count)
    interp_high_per = interpolate_by_distance(high_per_list, dist, interp_count)
    interp_low_per = interpolate_by_distance(low_per_list, dist, interp_count)
    return (interp_volume_per, interp_open_per, interp_close_per, interp_high_per, interp_low_per)


