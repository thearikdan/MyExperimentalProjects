import pickle



full_path = "/media/ara/Passport1_2TB/datasets/pyfin/data_v1/AMZN/2018-7-3/1m/AMZN_2018-7-3_1m.pickle"

f = open(full_path, "rb")

date_time, volume, opn, close, high, low = pickle.load(f)

f.close()

print len(date_time)
print date_time


#conn, cursor = db.connect_to_database("../database/database_settings.txt")


#db.insert_intraday_file_records_v1_into_database(conn, cursor, records)


#cursor.close()
#conn.close()

