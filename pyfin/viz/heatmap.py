#Needs pyfin virtualenv for matplotlib

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def show(data, mod):
    shape = np.shape(data)
    sns.set()

    # Draw a heatmap with the numeric values in each cell
    f, ax = plt.subplots(figsize=(9, 5))
    sns.heatmap(data, annot=True, fmt="f", linewidths=.5, ax=ax)
    plt.show()

