import sys
sys.path.insert(0, "../")


from input import read

name = '/media/ara/HDD/data/Finance/WEED.TO.10.22.17.11.22.17.csv'

my_data = read.get_all_data_from_file(name)
print my_data

headers = read.get_headers_from_file(name)
print headers

num_data = read.get_numeric_data_from_file(name)
print num_data

date = read.get_date_from_file(name)
print date

op = read.get_opening_price_from_file(name)
print op

hp = read.get_high_price_from_file(name)
print hp

lp = read.get_low_price_from_file(name)
print lp

cp = read.get_closing_price_from_file(name)
print cp

acp = read.get_adjusted_closing_price_from_file(name)
print acp

v = read.get_volume_from_file(name)
print v



