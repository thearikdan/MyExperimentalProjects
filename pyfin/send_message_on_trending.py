from utils import observation
from datetime import datetime, timedelta

from utils import observation
from datetime import datetime

import time, threading
import smtplib


symbol = "AMZN"
minutes_interval = 5

#check for average price velocity 0.5% per hour
percentage = 0.005 / 60 * minutes_interval
check_count = 2


def send_message_if_trending():
#    date_time = datetime.now() - timedelta(minutes = 5)
    date_time = datetime.now()
    trending = observation.is_intraday_trending(symbol, date_time, minutes_interval, percentage, check_count)
    if (trending):
        message = "%s %s is trending" % (date_time.strftime("%Y-%m-%d %H:%M"), symbol)
        server = smtplib.SMTP( "smtp.gmail.com", 587 )
        server.starttls()
        server.login( 'aramarketwatch@gmail.com', 'Watchmen' )
        server.sendmail( 'Market Watchmen', '4168733699@msg.telus.com', message )

    threading.Timer(minutes_interval * 60, send_message_if_trending).start()

send_message_if_trending()

