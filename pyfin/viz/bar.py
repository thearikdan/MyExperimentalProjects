#Needs pyfin virtualenv for matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
#import color_schema
#from matplotlib import colors



def get_x_from_data(data):
    shape = np.shape(data)
    x = np.arange(shape[0])
    width=[data[j][2] for j in range(len(x))]
    x[0] = 0
    for i in range (1, len(x)):
        s = np.sum(width[0:i])
        x[i] = s
    return x


def show(data):
    shape = np.shape(data)
    print shape
    x = get_x_from_data(data)
#    x = np.arange(shape[0])
    print x

    gain = data[:,1] - data[:,0]
    print gain

    width=[data[j][2] for j in range(len(x))]
    print width


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

#    ax.bar(x, df)
    ax.bar(x, gain,  width=[data[j][2] for j in range(len(x))])
    plt.show()

