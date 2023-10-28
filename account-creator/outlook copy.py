import imaplib
import email
from bs4 import BeautifulSoup
from email.header import decode_header

class Reddit_Verify:
    def outlook_mail(bot_number,email_id, passw):
            
        # Outlook IMAP server and login credentials
        outlook_server = "outlook.office365.com"
        email_address = email_id
        password = passw

        # Connect to Outlook's IMAP server
        try:
            imap = imaplib.IMAP4_SSL(outlook_server)
            imap.login(email_address, password)
            print(f'[{bot_number}] Mail_Handler: Logged in to Outlook')
        except Exception as e:
            print(f"[{bot_number}] Mail_Handler: Error login to Outlook: Account Locked.")
            return False

        # Select the mailbox you want to access (e.g., "inbox")
        mailbox = "inbox"
        imap.select(mailbox)

        # Search for the latest email
        try:
            status, email_ids = imap.search(None, "ALL")  # You can use other criteria like "UNSEEN" for unread emails
            email_ids = email_ids[0].split()
            print(f'[{bot_number}] Total mails in Inbox:',len(email_ids))
        except Exception as e:
            print(f"[{bot_number}] Error searching for emails: ", str(e))
            imap.logout()
            return False

        # check all emails with reversed order
        for email_id in reversed(email_ids):
            try:
                status, email_data = imap.fetch(email_id, "(RFC822)")
                raw_email = email_data[0][1]
                msg = email.message_from_bytes(raw_email)
                
                # Get email subject and sender
                subject, encoding = decode_header(msg["Subject"])[0]
                sender, encoding = decode_header(msg["From"])[0]
                try:
                    body = msg.get_payload(decode=True).decode()
                except:
                    pass
  
            except Exception as e:
                print(f"[{bot_number}] Error fetching email {email_id}: ", str(e))
                continue
            
            if 'Reddit' in sender:
                print(f'[{bot_number}] Mail_Handler: Reddit mail found')
                soup = BeautifulSoup(body, 'html.parser')
                links = soup.find_all('a')
                for link in links:
                    if 'verification' in str(link.get('href')):
                        print(f'[{bot_number}] Mail_Handler: Reddit verification link found')
                        imap.logout()
                        return str(link.get('href'))
            else:
                continue
            
        print(f'[{bot_number}] Mail_Handler: No Reddit mail found')
        # Logout and close the IMAP connection
        imap.logout()
        return False
    
link = Reddit_Verify.outlook_mail(1,'roten_pernett_334165@outlook.com','w-4hLrS5dv')
print(link)