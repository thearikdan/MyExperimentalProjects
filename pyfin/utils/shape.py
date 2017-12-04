import numpy as np
import constants



def pad_start(lst, days):
    start = int (days[0])

    for i in range(start):
        lst.insert(0, [constants.PADDED_DAY])
        days.insert(0, start - 1 - i)
    
    return lst, days



def insert_holidays(index, lst, days, diff, mod):
    if (diff == 1) or (diff == -(mod - 1)):
        return
    if (diff > 1):
        for i in range(diff - 1):
            days.insert((index + i), (index + i) % mod)
            lst.insert ((index + i), [constants.HOLIDAY])
    else: #diff is not positive
        count = mod - 1 - abs(diff)
        for i in range(count):
            days.insert((index + i), (index + i) % mod)
            lst.insert ((index + i), [constants.HOLIDAY])
    return lst, days  
            


def pad_holidays(lst, days, mod):
    l = len(days)
    for i in range (l-1):
        d0 = (int (days[i])) % mod
        d1 = (int (days[i + 1])) % mod
        diff = d1 - d0
        if (diff == 1) or (diff == -(mod - 1)):
            continue
        else:
            lst, days = insert_holidays(i + 1, lst, days, diff, mod)
    return lst, days



def pad_end(lst, mod):
    l = len(lst)

    rest = l % mod
    if (rest > 0):
        for i in range(mod - rest):
            lst.append([constants.PADDED_DAY])
    
    return lst



def reshape_data(data, days, mod):
    lst = data.tolist()

    lst, days = pad_start(lst, days)
    lst, days = pad_holidays(lst, days, mod)
    lst = pad_end(lst, mod)

    new_data = np.array(lst)

    data_shaped = new_data.reshape(-1, mod)
    sh = np.shape(data_shaped)
    return data_shaped

