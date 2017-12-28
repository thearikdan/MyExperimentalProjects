from read_write import read
from utils import constants
import numpy as np

def get_absolute_change_from_numeric_data(data):
    op = read.get_opening_price_from_numeric_data(data)

    cp = read.get_closing_price_from_numeric_data(data)

    diff = cp - op

    return diff


def get_max_absolute_change_from_numeric_data(data):
    op = read.get_opening_price_from_numeric_data(data)

    hp = read.get_high_price_from_numeric_data(data)

    diff = hp - op

    return diff


def get_min_absolute_change_from_numeric_data(data):
    op = read.get_opening_price_from_numeric_data(data)

    lp = read.get_low_price_from_numeric_data(data)

    diff = lp - op

    return diff


def get_mean_and_deviation_of_day(day_data):
    data = []
    sh = day_data.shape
    for i in range (sh[0]):
        if ((day_data[i] == constants.PADDED_DAY) or (day_data[i] == constants.HOLIDAY)):
            continue
        else:
            data.append(day_data[i])

    data_np = np.array(data)
    mean = np.mean(data_np)
    dev = np.std(data_np)

    return mean, dev

