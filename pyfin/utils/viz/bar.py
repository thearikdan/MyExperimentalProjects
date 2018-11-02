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


def draw_text(ax, rect):
    min_perc = 2.5

    clr = "white"
    yloc = rect.get_y()

    height = rect.get_height()
    perc = height / rect.get_y() * 100


    if abs(perc) > min_perc:
        clr = "white"
        yloc = rect.get_y() + height * 3 / 4
    else:
        clr = "black"
        yloc = rect.get_y() + height / 2

    p = "%.2f%%" % perc
    xloc = rect.get_x() + (rect.get_width() / 2.0)
#    ax.text(xloc, yloc, p, horizontalalignment='center', verticalalignment='center', color=clr, weight='bold')
    ax.text(xloc, yloc, p, horizontalalignment='center', verticalalignment='center', color=clr)

    if (abs(perc) > min_perc):
        days = rect.get_width()
        if (days > 1):
            p = "%d days" % days
        else:
            p = "%d" % days

        yloc = rect.get_y() + height / 4
        ax.text(xloc, yloc, p, horizontalalignment='center', verticalalignment='center', color=clr)


def show(data, title):
    shape = np.shape(data)
    x = get_x_from_data(data)
    c = get_color_from_data(data)

    gain = data[:,1] - data[:,0]

    w=[data[j][2] for j in range(len(x))]

    f, ax = plt.subplots(figsize=(shape[0], shape[1]))

    f.suptitle(title, fontsize=12)

    rects = ax.bar(x, gain, align="edge", bottom=data[:,0], width=w, color=c)

    ax.set_xlim(xmin=0)

    for rect in rects:
        draw_text(ax, rect)

    tick_end = x[len(x)-1] + int(w[len(x)-1])

    plt.xticks(np.arange(0, tick_end + 1, 1.0))
    plt.show()

