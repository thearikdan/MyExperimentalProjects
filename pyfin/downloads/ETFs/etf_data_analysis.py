from etf_utils import etf_utils as eu

ROOT_DIR = "etf_data"


etfs = eu.get_etf_list_from_directory(ROOT_DIR + "/Region")
print (etfs)

etfs = eu.get_etfs_in_dir_A_but_not_B(ROOT_DIR + "/Asset_Class", ROOT_DIR + "/Region")
print (etfs)
print (len(etfs))

etfs = eu.get_etfs_in_dir_A_but_not_B(ROOT_DIR + "/Sector", ROOT_DIR + "/Region")
print (etfs)
print (len(etfs))

etfs = eu.get_etfs_in_dir_A_but_not_B(ROOT_DIR + "/Volatility", ROOT_DIR + "/Region")
print (etfs)
print (len(etfs))

columns = eu.get_list_of_columns_from_directory(ROOT_DIR + "/Region")
for c in columns:
    print (c + "\n")

#Columns for db table ets: 'Symbol', 'ETF Name', 'Asset Class', 'Inverse', 'Leveraged', 'ETFdb.com Category', 'Inception'
