#source: https://stackoverflow.com/questions/43971138/python-plotting-colored-grid-based-on-values

import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import color_schema


def show(data, mod):
    shape = np.shape(data)

    bounds, colormap = color_schema.get_bounds_and_colormap()

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


