import imaplib
import email
from bs4 import BeautifulSoup
from email.header import decode_header

class Reddit_Verify:
    def outlook_mail(email_id, passw):
            
        # Outlook IMAP server and login credentials
        outlook_server = "outlook.office365.com"
        email_address = email_id
        password = passw

        # Connect to Outlook's IMAP server
        try:
            imap = imaplib.IMAP4_SSL(outlook_server)
            imap.login(email_address, password)
        except Exception as e:
            print("Error connecting to Outlook: ", str(e))
            exit(1)

        # Select the mailbox you want to access (e.g., "inbox")
        mailbox = "inbox"
        try:
            imap.select(mailbox)
        except Exception as e:
            print("Error selecting mailbox: ", str(e))
            imap.logout()
            exit(1)

        # Search for the latest email
        try:
            status, email_ids = imap.search(None, "ALL")  # You can use other criteria like "UNSEEN" for unread emails
            email_ids = email_ids[0].split()
            latest_email_id = email_ids[-1]
        except Exception as e:
            print("Error searching for emails: ", str(e))
            imap.logout()
            exit(1)

        # Fetch the latest email
        try:
            status, email_data = imap.fetch(latest_email_id, "(RFC822)")
            raw_email = email_data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            # Get email subject and sender
            subject, encoding = decode_header(msg["Subject"])[0]
            sender, encoding = decode_header(msg["From"])[0]
            body = msg.get_payload(decode=True).decode()
            
            # If you want to get the email body, you can use msg.get_payload() and decode it if necessary
            # email_body = msg.get_payload(decode=True).decode()
           
        except Exception as e:
            print("Error fetching latest email: ", str(e))

        # Logout and close the IMAP connection
        imap.logout()
        return subject, sender, body
