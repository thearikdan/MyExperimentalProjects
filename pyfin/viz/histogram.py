import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def show_time_hour_minute_histograpm(lst):

    fig, ax = plt.subplots(1)
    fig.autofmt_xdate()
    plt.hist(lst)

    xfmt = mdates.DateFormatter('%H:%M')
    ax.xaxis.set_major_formatter(xfmt)

    plt.show()


