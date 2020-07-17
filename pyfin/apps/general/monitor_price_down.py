import sys
sys.path.append("../..")

import json
import os
import numpy as np
import time, threading

from utils.web import download
from datetime import datetime, timedelta

import smtplib


def start_monitor(server, symbol, stop_price, email, password):
    print("1")
    threading.Timer(10, start_monitor, [server, symbol, stop_price, email, password]).start()
    start_date = datetime.now() - timedelta(minutes=5)
    end_date = datetime.now()
    print("2")

    is_data_available, date_time, volume, opn, close, high, low = download.get_intraday_data_from_web(symbol, start_date, end_date)
    print("2.5")

    if not is_data_available:
        print("2.75")
        return
    print("3")


    nones=[i for i in range(len(close)) if close[i] == None]
    print("4")

    clean_time = np.delete(date_time, nones)
    clean_close = np.delete(close, nones)

    last_time = clean_time[-1:][0].strftime("%m/%d/%Y, %H:%M:%S")
    price = clean_close[-1:][0]
    print(price)

    message = "Symbol " + symbol + " reached price " + str(price) + " at " + last_time
    print (message)
    print("5")
    if (price <= stop_price):
        print("6")
        server.sendmail('Markets Data Intelligence', '4168733699@msg.telus.com', message)
        print("7")


my_path = os.path.abspath(os.path.dirname(__file__))
settings_file_name = os.path.join(my_path, "../../utils/security/settings.json")
with open(settings_file_name) as json_file:
    settings = json.load(json_file)

print (settings["email"])
print (settings["email_password"])
server = smtplib.SMTP( "smtp.gmail.com", 587 )
server.starttls()
server.login( settings["email"], settings["email_password"])

start_monitor(server, "TQQQ", 113.5, settings["email"], settings["email_password"])