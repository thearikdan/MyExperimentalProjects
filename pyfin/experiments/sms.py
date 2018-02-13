import smtplib

# Establish a secure session with gmail's outgoing SMTP server using your gmail account
server = smtplib.SMTP( "smtp.gmail.com", 587 )

server.starttls()

server.login( 'aramarketwatch@gmail.com', 'Watchmen' )

# Send text message through SMS gateway of destination number
server.sendmail( 'Market Watchmen', '4168733699@msg.telus.com', 'Hello' )
