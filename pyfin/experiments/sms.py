'''
https://stackoverflow.com/questions/26852128/smtpauthenticationerror-when-sending-mail-using-gmail-and-python
Your code looks correct. Try logging in through your browser and if you are able to access your account come back and try your code again. Just make sure that you have typed your username and password correct

EDIT: Google blocks sign-in attempts from apps which do not use modern security standards (mentioned on their support page). You can however, turn on/off this safety feature by going to the link below:

Go to this link and select Turn On
https://www.google.com/settings/security/lesssecureapps
'''

import smtplib

# Establish a secure session with gmail's outgoing SMTP server using your gmail account
server = smtplib.SMTP( "smtp.gmail.com", 587 )

server.starttls()

server.login( 'marketsdataintelligence@gmail.com', 'Tam011374156' )

# Send text message through SMS gateway of destination number
server.sendmail( 'Markets Data Intelligence', '4168733699@msg.telus.com', 'Hello' )
