from numpy import genfromtxt

def get_all_data_from_file(filename):
    data = genfromtxt('/media/ara/HDD/data/Finance/WEED.TO.10.22.17.11.22.17.csv', dtype=None, delimiter=',')
    return data


def get_headers_from_file(filename):
    data = get_all_data_from_file(filename)
    return data[0]


def get_timeframe_from_file(filename):
    data = get_all_data_from_file(filename)
    return data[:,0:1]


def get_numerical_data_from_file(filename):
    data = get_all_data_from_file(filename)
    return data[1:,1:]

