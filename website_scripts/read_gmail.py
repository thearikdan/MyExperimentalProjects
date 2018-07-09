#https://codehandbook.org/how-to-read-email-from-gmail-using-python/

import smtplib
import time
import imaplib
import email

# -------------------------------------------------
#
# Utility to read email from Gmail Using Python
#
# ------------------------------------------------

def read_email_from_gmail(smtp_server, account, password, label):
    try:
        mail = imaplib.IMAP4_SSL(smtp_server)
        mail.login(account,password)
#        mail.select('inbox')
        mail.select(label)

        type, data = mail.search(None, 'ALL')
        mail_ids = data[0]

        id_list = mail_ids.split()   
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])


        for i in range(latest_email_id,first_email_id, -1):
            typ, data = mail.fetch(i, '(RFC822)' )

            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    email_subject = msg['subject']
                    email_from = msg['from']
                    print 'From : ' + email_from + '\n'
                    print 'Subject : ' + email_subject + '\n'

    except Exception, e:
        print str(e)



labels = ['Crime', 'Design', 'Fashion', 'Lifestyle', 'News', 'Transportation', 'Travel']

for label in labels:
    read_email_from_gmail("smtp.gmail.com", account, password, label)
