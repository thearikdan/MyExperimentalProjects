import numpy as np


def is_corrupt_value(a):
#    if (a == 0) or (a is None) or np.isnan(float(a)):
    if (a is None) or np.isnan(float(a)):
            return True
    else:
        return False


def find_next_good_value(lst, index):
    val = None
    count = len(lst)

    if (index >= count):
        return val

    for i in range(index + 1, count):
        if not is_corrupt_value(lst[i]):
            val = lst[i]
            return val
    return val



def get_corrupt_ratio(lst):
    corrupt_count = 0
    count = len(lst)
    if (count == 0):
        return corrupt_count

    for i in range(count):
        if is_corrupt_value(lst[i]):
            corrupt_count = corrupt_count + 1

    return float(corrupt_count) / count




def find_previous_good_value(lst, index):
    val = None
    count = len(lst)

    if (index >= count):
        return val

    if (index <= 0):
        return val

    for i in range(0, index - 1):
        if not is_corrupt_value(lst[i]):
            val = lst[i]
            return val
    return val


def heal_list(lst):
    count = len(lst)
    corrupt_ratio = get_corrupt_ratio(lst)
    for i in range(count):
        if is_corrupt_value(lst[i]):
            lst[i] = find_next_good_value(lst, i)
            if is_corrupt_value(lst[i]):
                lst[i] = find_previous_good_value(lst, i)
    return lst, corrupt_ratio


def heal_intraday_data(volume, opn, close, high, low):
    v, c_v = heal_list(volume)
    o, c_o = heal_list(opn)
    c, c_c = heal_list(close)
    h, c_h = heal_list(high)
    l, c_l = heal_list(low)
    return (v, o, c, h, l, c_v, c_o, c_c, c_h, c_l)

