import sys
sys.path.append("../..")

from utils.db import db
#import psycopg2


file_name = 'new_industries.txt'
industries = []

with open(file_name) as f:
    industries =  [line. rstrip('\n') for line in open(file_name)]

print(industries)

conn, cursor = db.connect_to_database("../database_settings.txt")

db.insert_names("public.industries", conn, cursor, industries)

conn.commit()
cursor.close()
conn.close()

