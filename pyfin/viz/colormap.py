#source: https://stackoverflow.com/questions/43971138/python-plotting-colored-grid-based-on-values

import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np


def show(data):
    shape = np.shape(data)

    # create discrete colormap
#    bounds = [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    bounds = []

    for i in xrange (-100, -30, 5):
        bounds.append(i / 10.)

    for i in xrange (-30, 30, 1):
        bounds.append(i / 10.)

    for i in xrange (30, 100, 5):
        bounds.append(i / 10.)
 
#    bounds = [-10, -9, -8, -7, -6, -5, -4, -3.5, -3, -2.5 -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, #3, 3.5, 4, 5, 6, 7, 8, 9, 10]
#    print bounds
    count = len(bounds)

    colormap = []
    step = 1. / (count / 2)

    for i in range (count / 2):
        c = [1.0, i * step, i * step]
        colormap.append(c)

    c = [1., 1., 1.]
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
    ax.set_xticks(np.arange(-0.5, shape[0]-0.5, 1));
    ax.set_yticks(np.arange(-0.5, shape[1]-0.5, 1));

    plt.show()

