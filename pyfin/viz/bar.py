#Needs pyfin virtualenv for matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np



def get_x_from_data(data):
    shape = np.shape(data)
    x = np.arange(shape[0])
    width=[data[j][2] for j in range(len(x))]
    x[0] = 0
    for i in range (1, len(x)):
        s = np.sum(width[0:i])
        x[i] = s
    return x

def get_color_from_data(data):
    c = []
    gain = data[:,1] - data[:,0]
    for i in range (len(gain)):
        if (gain[i] < 0):
            c.append("red")
        else:
            c.append("green")
    return c


def show(data):
    shape = np.shape(data)
    x = get_x_from_data(data)
    c = get_color_from_data(data)

    gain = data[:,1] - data[:,0]

    w=[data[j][2] for j in range(len(x))]

    f, ax = plt.subplots(figsize=(shape[0], shape[1]))
    ax.bar(x, gain, bottom=data[:,0], width=w, color=c)
    plt.show()

