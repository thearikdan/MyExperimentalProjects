from input import read

name = '/media/ara/HDD/data/Finance/WEED.TO.10.22.17.11.22.17.csv'

my_data = read.get_all_data_from_file(name)
print my_data

headers = read.get_headers_from_file(name)
print headers

num_data = read.get_numerical_data_from_file(name)
print num_data

time_frame = read.get_timeframe_from_file(name)
print time_frame


