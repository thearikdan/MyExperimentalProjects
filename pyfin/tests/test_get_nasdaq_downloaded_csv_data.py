import sys
sys.path.append("..")

from utils import file_op


file_name = '/media/ara/HDD/MyProjects/pyfin/downloads/nasdaq-july-22-2018csv'

symbols, names, last_sales, market_caps, ipo_years, sectors, industries, summary_quotes = file_op.get_nasdaq_downloaded_csv_data(file_name)

print symbols
print"_______________________________________"

print names
print"_______________________________________"

print last_sales
print"_______________________________________"

print market_caps
print"_______________________________________"

print ipo_years
print"_______________________________________"

print sectors
print"_______________________________________"

print industries
print"_______________________________________"

print summary_quotes
print"_______________________________________"

