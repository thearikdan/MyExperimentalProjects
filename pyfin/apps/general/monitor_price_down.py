import sys
sys.path.append("../..")

import json
import os
import numpy as np
import time, threading

from utils.web import download
from datetime import datetime, timedelta

import smtplib
from email.mime.text import MIMEText


stop_event = threading.Event()
limit_event = threading.Event()


def start_monitor(server, symbol, stop_price, limit_price, email, password):
    timer = threading.Timer(10, start_monitor, [server, symbol, stop_price, limit_price, email, password])
    timer.start()
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

    message = "\nSymbol " + symbol + " reached price " + str(price) + " at " + last_time
    print (message)
    if not stop_event.is_set():
        if (price <= stop_price):
            #insert blank line for semicolon https://stackoverflow.com/questions/7294885/python-emailing-use-of-colon-causes-no-output            
            message = "\nSymbol " + symbol + " reached stop price " + str(price) + " at " + last_time


#            message = "Symbol " + symbol + " reached stop price " + str(price)
            print(message)
            server.sendmail('Markets Data Intelligence', '4168733699@msg.telus.com', message)
            
            stop_event.set()
    
    elif stop_event.is_set() and not limit_event.is_set():
        if (price <= limit_price):
            message = "\nSymbol " + symbol + " reached limit price " + str(price) + " at " + last_time
            print(message)
            server.sendmail('Markets Data Intelligence', '4168733699@msg.telus.com', message)
            
            limit_event.set()
    
    elif stop_event.is_set() and limit_event.is_set():
        message = "\nStopped monitoring the price because limit was reached."
        print (message)
        server.sendmail('Markets Data Intelligence', '4168733699@msg.telus.com', message)
        timer.cancel()
        timer.join()


my_path = os.path.abspath(os.path.dirname(__file__))
settings_file_name = os.path.join(my_path, "../../utils/security/settings.json")
with open(settings_file_name) as json_file:
    settings = json.load(json_file)


stop_price = float(input('Enter stop price: '))
limit_price = float(input('Enter limit price: '))

print ("Started monitoring for stop price " + str(stop_price) + " and limit price " + str(limit_price))
server = smtplib.SMTP( "smtp.gmail.com", 587 )
server.starttls()
server.login( settings["email"], settings["email_password"])

start_monitor(server, "TQQQ", stop_price, limit_price, settings["email"], settings["email_password"])
