import sys
sys.path.append("..")

from utils import file_op, db
import psycopg2


file_name = '/media/ara/HDD/MyProjects/pyfin/downloads/nasdaq-july-22-2018csv'
symbols, names, last_sales, market_caps, ipo_years, sectors, industries, summary_quotes = file_op.get_nasdaq_downloaded_csv_data(file_name)
ind_names = set(industries)
print ind_names

conn, cursor = db.connect_to_database("database_settings.txt") 

for ind in ind_names:
#    sql = "INSERT INTO public.industries(name) VALUES('"+ind+"');"
    sql = "INSERT INTO public.industries(name) VALUES('"+ind+"') WHERE NOT EXISTS (SELECT * FROM public.industries WHERE name='"+ind+"');"
    print sql
    cursor.execute(sql)
conn.commit()
cursor.close()
conn.close()

