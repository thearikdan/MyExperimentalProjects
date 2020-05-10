def get_last_drop_index(price_list, ind):
    count = len(price_list)
    for i in range (ind, count - 1):
        if price_list[i + 1] < price_list[i]:
            continue
        else:
            return (i)


def get_first_drop_index(price_list, ind):
    count = len(price_list)
    for i in range (ind, count - 1):
        if price_list[i + 1] < price_list[i]:
            return i
    return -1


def get_next_drop(price_list, ind):
    count = len(price_list)
    if ind == count - 1:
        return ()
    for i in range (ind, count - 1):
        k = get_first_drop_index(price_list, i)
        if k == -1:
            return ()
        l = get_last_drop_index(price_list, k + 1)
        return (k, l)



def get_drop_list(price_list):
    drop_list = []
    count = len(price_list)
    i = 0
    while i < count:
        drop = get_next_drop(price_list, i)
        if None in drop:
            break
        if len(drop) > 0:
            drop_list.append(drop)
            i = drop[1]
        else:
            i = i + 1
    return drop_list


def get_percentages_from_list(price_list, ls):
    count = len(ls)
    perc_list = []
    for i in range (count):
        start = price_list[ls[i][0]]
        end = price_list[ls[i][1]]
        perc = (end - start) * 100.0 / start
        perc_list.append(perc)
    return perc_list


def get_drop_stats(price_list):
    drop_list = get_drop_list(price_list)
    percentages = get_percentages_from_list(price_list, drop_list)
    return drop_list, percentages
