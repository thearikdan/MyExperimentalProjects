import sys
sys.path.append("..")

from utils import file_op, db
import psycopg2


file_name1 = '/media/ara/HDD/MyProjects/pyfin/downloads/nasdaq-july-22-2018.csv'
file_name2 = '/media/ara/HDD/MyProjects/pyfin/downloads/nyse-july-22-2018.csv'
file_name3 = '/media/ara/HDD/MyProjects/pyfin/downloads/amex-july-22-2018.csv'

symbols1, names1, last_sales1, market_caps1, ipo_years1, sectors1, industries1, summary_quotes1 = file_op.get_nasdaq_downloaded_csv_data(file_name1)
symbols2, names2, last_sales2, market_caps2, ipo_years2, sectors2, industries2, summary_quotes2 = file_op.get_nasdaq_downloaded_csv_data(file_name2)
symbols3, names3, last_sales3, market_caps3, ipo_years3, sectors3, industries3, summary_quotes3 = file_op.get_nasdaq_downloaded_csv_data(file_name3)

ind_names1 = list(set(industries1[1:len(industries1)]))
ind_names2 = list(set(industries2[1:len(industries2)]))
ind_names3 = list(set(industries3[1:len(industries3)]))

conn, cursor = db.connect_to_database("database_settings.txt") 

db.insert_names("public.industries", cursor, ind_names1)
db.insert_names("public.industries", cursor, ind_names2)
db.insert_names("public.industries", cursor, ind_names3)

conn.commit()
cursor.close()
conn.close()

