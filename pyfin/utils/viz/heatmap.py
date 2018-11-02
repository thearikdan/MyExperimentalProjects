#Needs pyfin virtualenv for matplotlib
#%matplotlib inline

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import color_schema
from matplotlib import colors

def show(data, title, mod):
    shape = np.shape(data)

    bounds, colormap = color_schema.get_bounds_and_colormap()

    cmap = colors.ListedColormap(colormap)
    norm = colors.BoundaryNorm(bounds, cmap.N)

    # Create a dataset (fake)
    df = pd.DataFrame(data, columns=["Mon","Tue","Wed","Thu","Fri"])

    # Draw a heatmap with the numeric values in each cell
    f, ax = plt.subplots(figsize=(shape[0], shape[1]), dpi=120)
    f.suptitle(title, fontsize=12)
    sns.heatmap(df, annot=True, fmt=".2f", linewidths=.5, ax=ax, cmap=cmap, norm=norm)
    plt.show()

