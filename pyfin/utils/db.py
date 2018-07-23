import psycopg2
import sys
 
def connect_to_database(settings_file_name):
    with open(settings_file_name) as f:
        lines = f.readlines()
    
    #Define our connection string
    conn_string = "host=" + lines[0] + " dbname=" + lines[1] + " user=" + lines[2] + " password=" + lines[3]
 
    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)
 
    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()
    print "Connected!\n"

    return conn, cursor

