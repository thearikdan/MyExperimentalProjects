import numpy as np


def is_corrupt_value(a):
    if (a == 0) or (a is None) or np.isnan(float(a)):
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
    for i in range(count):
        if is_corrupt_value(lst[i]):
            lst[i] = find_next_good_value(lst, i)
            if (lst[i] is None):
                lst[i] = find_previous_good_value(lst, i)
    return lst


def heal_intraday_data(volume, opn, close, high, low):
    v = heal_list(volume)
    o = heal_list(opn)
    c = heal_list(close)
    h = heal_list(high)
    l = heal_list(low)
    return (v, o, c, h, l)

