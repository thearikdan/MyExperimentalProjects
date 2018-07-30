import sys
sys.path.append("..")

from utils import file_op, db
import psycopg2


def get_company_data_from_table_list(symbols, names, ipo_years, sectors, industries, summary_quotes):
    syms = symbols[1:len(symbols)]
    nams = names[1:len(names)]
    ipos = ipo_years[1:len(ipo_years)]
    secs = sectors[1:len(sectors)]
    inds = industries[1:len(industries)]
    quos = summary_quotes[1:len(summary_quotes)]
    return syms, nams, ipos, secs, inds, quos



file_name1 = '/media/ara/HDD/MyProjects/pyfin/downloads/nasdaq-july-22-2018.csv'
file_name2 = '/media/ara/HDD/MyProjects/pyfin/downloads/nyse-july-22-2018.csv'
file_name3 = '/media/ara/HDD/MyProjects/pyfin/downloads/amex-july-22-2018.csv'

symbols1, names1, last_sales1, market_caps1, ipo_years1, sectors1, industries1, summary_quotes1 = file_op.get_nasdaq_downloaded_csv_data(file_name1)
symbols2, names2, last_sales2, market_caps2, ipo_years2, sectors2, industries2, summary_quotes2 = file_op.get_nasdaq_downloaded_csv_data(file_name2)
symbols3, names3, last_sales3, market_caps3, ipo_years3, sectors3, industries3, summary_quotes3 = file_op.get_nasdaq_downloaded_csv_data(file_name3)


symbols1, names1, ipo_years1, sectors1, industries1, summary_quotes1 = get_company_data_from_table_list(symbols1, names1, ipo_years1, sectors1, industries1, summary_quotes1)
symbols2, names2, ipo_years2, sectors2, industries2, summary_quotes2 = get_company_data_from_table_list(symbols2, names2, ipo_years2, sectors2, industries2, summary_quotes2)
symbols3, names3, ipo_years3, sectors3, industries3, summary_quotes3 = get_company_data_from_table_list(symbols3, names3, ipo_years3, sectors3, industries3, summary_quotes3)

conn, cursor = db.connect_to_database("database_settings.txt")

db.insert_companies("public.companies", cursor, symbols1, names1, ipo_years1, sectors1, industries1, summary_quotes1, ["nasdaq"]*len(symbols1))
db.insert_companies("public.companies", cursor, symbols2, names2, ipo_years2, sectors2, industries2, summary_quotes2,["nyse"]*len(symbols2))
db.insert_companies("public.companies", cursor, symbols3, names3, ipo_years3, sectors3, industries3, summary_quotes3, ["amex"]*len(symbols3))

conn.commit()
cursor.close()
conn.close()

