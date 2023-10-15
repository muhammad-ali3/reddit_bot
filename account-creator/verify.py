import imaplib
from seleniumwire import webdriver
from driver import get_driver_with_proxy_and_profile
import email
from bs4 import BeautifulSoup
from email.header import decode_header
import pandas as pd
from essentials import get_proxy
import os
import time

def outlook_mail(email_address, password): 
    # Outlook IMAP server and login credentials
    outlook_server = "outlook.office365.com"

    # Connect to Outlook's IMAP server
    try:
        imap = imaplib.IMAP4_SSL(outlook_server)
        imap.login(email_address, password)
        print('Mail_Handler: Logged in to Outlook')
    except Exception as e:
        print("Mail_Handler: Error login to Outlook: Account Locked")
        exit(1)

    # Select the mailbox you want to access (e.g., "inbox")
    mailbox = "inbox"
    imap.select(mailbox)

    # Search for the latest email
    try:
        status, email_ids = imap.search(None, "ALL")  # You can use other criteria like "UNSEEN" for unread emails
        email_ids = email_ids[0].split()
        print('Total mails in Inbox:',len(email_ids))
    except Exception as e:
        print("Error searching for emails: ", str(e))
        imap.logout()
        exit(1)

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
            print(f"Error fetching email {email_id}: ", str(e))
        
        if 'Reddit' in sender:
            print('Mail_Handler: Reddit mail found')
            soup = BeautifulSoup(body, 'html.parser')
            links = soup.find_all('a')
            for link in links:
                if 'verification' in str(link.get('href')):
                    print('Mail_Handler: Reddit verification link found')
                    imap.logout()
                    return str(link.get('href'))
        else:
            continue
        
    print('Mail_Handler: No Reddit mail found')
    # Logout and close the IMAP connection
    imap.logout()
    return False

if __name__ == '__main__':
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    accounts_path = os.path.join(base, 'assets', 'accounts.csv')
    # read accounts.csv
    if not os.path.exists(accounts_path):
        print('accounts.csv does not exist')
        exit(1)
    print('Mail_Handler: Reading accounts.csv')
    print('Mail_Handler: Checking for unverified accounts')
    accounts = pd.read_csv(accounts_path)
    for index, row in accounts.iterrows():
        if row['is_verified'] == 0:
            print('Mail_Handler: Unverified account found')
            username = row['username']
            password = row['password']
            email_address = row['email']
            proxy_username = row['proxy']
            date = row['date_created']
            print(f'Mail_Handler: Username: {username}')
            # data format is 08-10-2023 06:18:24
            date_created = time.mktime(time.strptime(date, '%d-%m-%Y %H:%M:%S'))
            current_time = time.time()
            passed_time = current_time - date_created
            print(passed_time)
            # check if 18 hours have passed 
            if passed_time > 64800:
                print('Mail_Handler: 24 hours have not passed')
                print('Mail_Handler: Link is now useless Skipping account')
                continue
            print('Mail_Handler: Checking for verification mail')
            verification_link = outlook_mail(email_address, password)
            if verification_link:
                print('Mail_Handler: Verification link found')
                proxy = get_proxy(proxy_username)
                if proxy is not False:
                    driver =get_driver_with_proxy_and_profile(proxy.split(':')[0], proxy.split(':')[1], proxy.split(':')[2], proxy.split(':')[3].strip(), username)
                    time.sleep(5)
                    driver.get(verification_link)
                    time.sleep(10)
                    accounts.loc[index, 'is_verified'] = 1
                    accounts.to_csv(accounts_path, index=False)
                    print('Mail_Handler: Account verified')
                else:
                    print('Mail_Handler: Proxy not found in database')
                    continue
            else:
                print('Mail_Handler: No verification mail found')
                continue
        