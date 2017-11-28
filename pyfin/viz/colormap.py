#source: https://stackoverflow.com/questions/43971138/python-plotting-colored-grid-based-on-values

import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

PADDED_DAY = -1000000.
PADDED_DAY_COLOR = [0., 0., 1.]

HOLIDAY = -500000.
HOLIDAY_COLOR = [0., 0., 0.5]
#HOLIDAY_COLOR = [1., 1., 0.]

BORDER = 5000.



def pad_start(lst, days):
    start = int (days[0])

    for i in range(start):
        lst.insert(0, [PADDED_DAY])
        days.insert(0, start - 1 - i)
    
    return lst, days



def insert_holidays(index, lst, days, diff, mod):
    if (diff == 1) or (diff == -(mod - 1)):
        return
    if (diff > 1):
        for i in range(diff - 1):
            days.insert((index + i), (index + i) % mod)
            lst.insert ((index + i), [HOLIDAY])
    else: #diff is not positive
        count = mod - 1 - abs(diff)
        for i in range(count):
            days.insert((index + i), (index + i) % mod)
            lst.insert ((index + i), [HOLIDAY])
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
            lst.append([PADDED_DAY])
    
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

    

def show(data, mod):
    shape = np.shape(data)

    # create discrete colormap
#   bounds = [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#   bounds = [-20, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20]

    bounds = []
    bounds.append(PADDED_DAY)
    bounds.append(HOLIDAY - BORDER)


    for i in xrange (-1000, -300, 100):
        bounds.append(i / 10.)

    for i in xrange (-300, -100, 10):
        bounds.append(i / 10.)

    for i in xrange (-100, -50, 5):
        bounds.append(i / 10.)

    for i in xrange (-50, 50, 1):
        bounds.append(i / 10.)

    for i in xrange (50, 100, 5):
        bounds.append(i / 10.)

    for i in xrange (100, 300, 10):
        bounds.append(i / 10.)

    for i in xrange (300, 1000, 100):
        bounds.append(i / 10.)

    count = len(bounds) - 2

    colormap = []
    c = PADDED_DAY_COLOR
    colormap.append(c)
    c = HOLIDAY_COLOR
    colormap.append(c)

    step = 1. / (count / 2)

    for i in range (1, count / 2):
        c = [1.0, i * step, i * step]
        colormap.append(c)

    for i in range (count / 2 + 1, count):
        c = [2 - (i + 1) * step, 1, 2 - (i + 1) * step]
#        c = [2 - (i) * step, 1, 2 - (i) * step]
        colormap.append(c)


#    print colormap

    cmap = colors.ListedColormap(colormap)
    norm = colors.BoundaryNorm(bounds, cmap.N)

    fig, ax = plt.subplots()
    ax.imshow(data, cmap=cmap, norm=norm)

    # draw gridlines
    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
#    ax.set_xticks(np.arange(-0.5, shape[0] + 0.5, 1));
    ax.set_xticks(np.arange(-0.5, mod, 1));
    ax.set_yticks(np.arange(-0.5, shape[0], 1));

    plt.show()


