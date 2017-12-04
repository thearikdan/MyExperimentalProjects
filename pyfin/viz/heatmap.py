#Needs pyfin virtualenv for matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import color_schema
from matplotlib import colors

def show(data, mod):
    shape = np.shape(data)

    bounds, colormap = color_schema.get_bounds_and_colormap()

    cmap = colors.ListedColormap(colormap)
    norm = colors.BoundaryNorm(bounds, cmap.N)

    # Create a dataset (fake)
    df = pd.DataFrame(data, columns=["Mon","Tue","Wed","Thu","Fri"])


    # Draw a heatmap with the numeric values in each cell
    f, ax = plt.subplots(figsize=(shape[0], shape[1]))
    sns.heatmap(df, annot=True, fmt="f", linewidths=.5, ax=ax, cmap=cmap, norm=norm)
    plt.show()

