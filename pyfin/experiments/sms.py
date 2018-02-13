import smtplib

# Establish a secure session with gmail's outgoing SMTP server using your gmail account
server = smtplib.SMTP( "smtp.gmail.com", 587 )

server.starttls()

server.login( 'arikdan@gmail.com', 'YourPassword' )

# Send text message through SMS gateway of destination number
server.sendmail( '"Ara', 'Your phone@your provider', 'Hello' )
