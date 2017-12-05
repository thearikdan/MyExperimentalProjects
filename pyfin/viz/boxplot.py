#Needs pyfin virtualenv for matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
#import color_schema
#from matplotlib import colors

def show(data):
    shape = np.shape(data)

#    bounds, colormap = color_schema.get_bounds_and_colormap()

#    cmap = colors.ListedColormap(colormap)
#    norm = colors.BoundaryNorm(bounds, cmap.N)

    # Create a dataset (fake)
    df = pd.DataFrame(data, columns=["Open","Close","Days"])
#    df = pd.DataFrame(data)


    # Draw a heatmap with the numeric values in each cell
    f, ax = plt.subplots(figsize=(shape[0], shape[1]))
#    f.suptitle(title, fontsize=12)
#    sns.boxplot(df, annot=True, fmt="f", linewidths=.5, ax=ax, cmap=cmap, norm=norm)
#    sns.boxplot(data=df)
#    kwargs['align'] = kwargs.get('align', 'center')

    ax.bar(df)
    plt.show()

