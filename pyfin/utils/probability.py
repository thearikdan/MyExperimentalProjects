import numpy as np
import constants

def get_positive_probability_of_day(day_data):
    sh = day_data.shape
    total_count = 0
    pos_count = 0
    for i in range (sh[0]):
        if ((day_data[i] == constants.PADDED_DAY) or (day_data[i] == constants.HOLIDAY)):
            continue
        elif(day_data[i] > 0):
            total_count = total_count + 1
            pos_count = pos_count + 1
        else:
            total_count = total_count + 1

    prob = float(pos_count) / total_count
    return prob

