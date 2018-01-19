import matplotlib.pyplot as plt


def show(count, start_date, end_date, title, subtitles, x_list, y_list, reference):

    plt.figure(1)

    left  = 0.125  # the left side of the subplots of the figure
    right = 0.9    # the right side of the subplots of the figure
    bottom = 0.1   # the bottom of the subplots of the figure
    top = 0.9      # the top of the subplots of the figure
    wspace = 0.2   # the amount of width reserved for space between subplots,
               # expressed as a fraction of the average axis width
    hspace = 1.5   # the amount of height reserved for space between subplots,
               # expressed as a fraction of the average axis height

    plt.subplots_adjust(left, bottom, right, top,
                wspace, hspace)

    plt.suptitle(title, fontsize=12)

    for i in range(count):
        ax = plt.subplot(count*100 + 11 + i)
        ax.set_title(subtitles[i], fontsize=10)
        plt.plot(x_list[i], y_list[i])
        plt.plot(x_list[i], reference, 'r')

    plt.show()


