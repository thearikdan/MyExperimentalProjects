from utils import db

conn, cursor = db.connect_to_database("database/database_settings.txt")

sql = "SELECT company_id, date, time, volume, opening_price, closing_price, high_price, low_price FROM intraday_prices;"
cursor.execute(sql)
rows = cursor.fetchall()
for row in rows:
    print row[0]
    print row[1]
    print row[2]
    print row[3]
    print row[4]
    print row[5]
    print row[6]
    print row[7]

    sql1 = "INSERT INTO intraday_prices_new (company_id, date, time, volume, opening_price, closing_price, high_price, low_price) VALUES('" + str(row[0]) + "','" + str(row[1]) + "'::date,'" + str(row[2]) + "'::time" + ",'" + str(row[3]) + "','" + str(row[4]) + "','" + str(row[5]) + "','" + str(row[6]) + "','" + str(row[7]) + "');"
    print sql1
    cur.execute(sql1)


conn.commit()
cursor.close()
conn.close()


