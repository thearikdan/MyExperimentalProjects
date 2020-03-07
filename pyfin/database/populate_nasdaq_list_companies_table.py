import sys
sys.path.append("..")

from utils import file_op
from utils.db import db
import psycopg2


#donload
#nasdaq https://datahub.io/core/nasdaq-listings
#nyse https://datahub.io/core/nyse-other-listings
#amex http://eoddata.com/stocklist/AMEX.htm
#eodata login aradan t-3

#The problem with the data is that these lists are not changing in years. Tried to run the same script one year later, and all companies are already in database!

def get_company_data_from_table_list(symbols, names, ipo_years, sectors, industries, summary_quotes):
    syms = symbols[1:len(symbols)]
    nams = names[1:len(names)]
    ipos = ipo_years[1:len(ipo_years)]
    secs = sectors[1:len(sectors)]
    inds = industries[1:len(industries)]
    quos = summary_quotes[1:len(summary_quotes)]
    return syms, nams, ipos, secs, inds, quos



file_name1 = '/media/ara/HDD/MyProjects/pyfin/downloads/nasdaq-listed_csv_mar_7_2020.csv'
file_name2 = '/media/ara/HDD/MyProjects/pyfin/downloads/nyse-listed_csv_mar_7_2020.csv'
file_name3 = '/media/ara/HDD/MyProjects/pyfin/downloads/AMEX_mar_7_2020.txt'

symbols1, names1, _, _, _, _, _ = file_op.get_nasdaq_downloaded_csv_data_2(file_name1)
symbols2, names2,  _, _, _, _, _ = file_op.get_nasdaq_downloaded_csv_data_2(file_name2)
symbols3, names3 = file_op.get_amex_downloaded_txt_data_2(file_name3)


#symbols1, names1, ipo_years1, sectors1, industries1, summary_quotes1 = get_company_data_from_table_list(symbols1, names1, ipo_years1, sectors1, industries1, summary_quotes1)
#symbols2, names2, ipo_years2, sectors2, industries2, summary_quotes2 = get_company_data_from_table_list(symbols2, names2, ipo_years2, sectors2, industries2, summary_quotes2)
#symbols3, names3, ipo_years3, sectors3, industries3, summary_quotes3 = get_company_data_from_table_list(symbols3, names3, ipo_years3, sectors3, industries3, summary_quotes3)


symbols1, names1, ipo_years1, sectors1, industries1, summary_quotes1 = get_company_data_from_table_list(symbols1, names1, "", "", "", "",)
symbols2, names2, ipo_years2, sectors2, industries2, summary_quotes2 = get_company_data_from_table_list(symbols2, names2, "", "", "", "",)
symbols3, names3, ipo_years3, sectors3, industries3, summary_quotes3 = get_company_data_from_table_list(symbols3, names3, "", "", "", "",)

conn, cursor = db.connect_to_database("database_settings.txt")

#db.insert_companies("public.companies", cursor, symbols1, names1, ipo_years1, sectors1, industries1, summary_quotes1, ["nasdaq"]*len(symbols1))
#db.insert_companies("public.companies", cursor, symbols2, names2, ipo_years2, sectors2, industries2, summary_quotes2,["nyse"]*len(symbols2))
#db.insert_companies("public.companies", cursor, symbols3, names3, ipo_years3, sectors3, industries3, summary_quotes3, ["amex"]*len(symbols3))

db.insert_companies("public.companies", conn, cursor, symbols1, names1, ["n/a"]*len(symbols1), ["n/a"]*len(symbols1), ["n/a"]*len(symbols1),["n/a"]*len(symbols1), [1]*len(symbols1))
db.insert_companies("public.companies", conn, cursor, symbols2, names2, ["n/a"]*len(symbols2), ["n/a"]*len(symbols2), ["n/a"]*len(symbols2),["n/a"]*len(symbols2),[2]*len(symbols2))
db.insert_companies("public.companies", conn, cursor, symbols3, names3, ["n/a"]*len(symbols3), ["n/a"]*len(symbols3), ["n/a"]*len(symbols3),["n/a"]*len(symbols3), [3]*len(symbols3))


conn.commit()
cursor.close()
conn.close()

