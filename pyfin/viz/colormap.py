#source: https://stackoverflow.com/questions/43971138/python-plotting-colored-grid-based-on-values

import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
from utils import constants


def show(data, mod):
    shape = np.shape(data)

    # create discrete colormap
#   bounds = [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#   bounds = [-20, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20]

    bounds = []
    bounds.append(constants.PADDED_DAY)
    bounds.append(constants.HOLIDAY - constants.BORDER)


    for i in xrange (-1000, -300, 100):
        bounds.append(i / 10.)

    for i in xrange (-300, -100, 10):
        bounds.append(i / 10.)

    for i in xrange (-100, -50, 5):
        bounds.append(i / 10.)

    for i in xrange (-50, -20, 2):
        bounds.append(i / 10.)

    for i in xrange (-20, 20, 1):
        bounds.append(i / 10.)

    for i in xrange (20, 50, 2):
        bounds.append(i / 10.)

    for i in xrange (50, 100, 5):
        bounds.append(i / 10.)

    for i in xrange (100, 300, 10):
        bounds.append(i / 10.)

    for i in xrange (300, 1000, 100):
        bounds.append(i / 10.)

    count = len(bounds) - 2

#    print bounds

    colormap = []
    c = constants.PADDED_DAY_COLOR
    colormap.append(c)
    c = constants.HOLIDAY_COLOR
    colormap.append(c)

    step = 1. / (count / 2)

    for i in range (0, count / 2):
        c = [1.0, i * step, i * step]
        colormap.append(c)

    for i in range (count / 2 + 1, count):
        c = [2 - (i + 1) * step, 1, 2 - (i + 1) * step]
        colormap.append(c)


#    print colormap

    cmap = colors.ListedColormap(colormap)
    norm = colors.BoundaryNorm(bounds, cmap.N)

    fig, ax = plt.subplots()
    ax.imshow(data, cmap=cmap, norm=norm)

    # draw gridlines
    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
    ax.set_xticks(np.arange(-0.5, mod, 1));
    ax.set_yticks(np.arange(-0.5, shape[0], 1));

    plt.show()


