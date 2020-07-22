import sys
sys.path.append("../..")
import json
import os
import numpy as np
import time, threading
from utils.web import download
from datetime import datetime, timedelta
import smtplib

rrsp_count = 3134
inv_count = 1232
tfsa_count = 666


def start_monitor(server, symbol, stop_price, limit_price, email, password):
    global stop_reached
    global limit_reached

    threading.Timer(10, start_monitor, [server, symbol, stop_price, limit_price, email, password]).start()
    start_date = datetime.now() - timedelta(minutes=5)
    end_date = datetime.now()
    

    is_data_available, date_time, volume, opn, close, high, low = download.get_intraday_data_from_web(symbol, start_date, end_date)

    if not is_data_available:
        return


    nones=[i for i in range(len(close)) if close[i] == None]

    clean_time = np.delete(date_time, nones)
    clean_close = np.delete(close, nones)

    last_time = clean_time[-1:][0].strftime("%m/%d/%Y, %H:%M:%S")
    price = clean_close[-1:][0]
    
    message = "Symbol " + symbol + " reached price " + str(price) + " at " + last_time
    print (message)
    if not stop_reached:
        if (price <= stop_price):
            message = "Symbol " + symbol + " reached stop price " + str(price) + " at " + last_time
            server.sendmail('Markets Data Intelligence', '4168733699@msg.telus.com', message)
            stop_reached = True
            
    if not limit_reached:
        if (price <= limit_price):
            message = "Symbol " + symbol + " reached limit price " + str(price) + " at " + last_time
            server.sendmail('Markets Data Intelligence', '4168733699@msg.telus.com', message)
            limit_reached = True
            exit(0)


my_path = os.path.abspath(os.path.dirname(__file__))
settings_file_name = os.path.join(my_path, "../../utils/security/settings.json")
with open(settings_file_name) as json_file:
    settings = json.load(json_file)


price = float(input('Enter a price: '))
stop = float(input('Enter stop percentage: '))
limit = float(input('Enter limit percentage: '))

stop_price = price * (1 - stop / 100.)
limit_price = price * (1 - limit / 100.)

print("\n")
print ('{} {}'.format('Stop price: ', stop_price))
print ('{} {}'.format('Limit price: ', limit_price))
print("\n")
print ('{} {}'.format('Current RRSP count: ', rrsp_count))
print ('{} {}'.format('Current Investment count: ', inv_count))
print ('{} {}'.format('Current TFSA count: ', tfsa_count))
print("\n")
print ('{} {}'.format('Estimated RRSP count: ', rrsp_count * stop_price / limit_price))
print ('{} {}'.format('Estimated Investment count: ', inv_count * stop_price / limit_price))
print ('{} {}'.format('Estimated TFSA count: ', tfsa_count * stop_price / limit_price))

server = smtplib.SMTP( "smtp.gmail.com", 587 )
server.starttls()
server.login( settings["email"], settings["email_password"])

start_monitor(server, "TQQQ", stop_price, limit_price, settings["email"], settings["email_password"])
