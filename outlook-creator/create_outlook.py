from seleniumwire import webdriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ChromeOptions
import os
import sys
import random
import requests
import base64
import time
import csv
import re
from onest_captcha import OneStCaptchaClient
from bs4 import BeautifulSoup
def create_driver_with_proxy(proxy_host, proxy_port, proxy_username, proxy_password):
    # Set up Selenium-Wire options for the proxy
    proxy_options = {
        'proxy': {
            'http': f'http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}',
            'https': f'https://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}',
            'no_proxy': 'localhost,127.0.0.1',  # Add any addresses you don't want to proxy
        }
    }
    options = ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--log-level=3')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-extensions")
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    driver = uc.Chrome(options=options, seleniumwire_options=proxy_options)
    return driver

def make_activity():
    # get span with id="id__355"
    span = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'span#id__355'))
    )
    span.click()

def solve_funcaptcha(driver):
    time.sleep(10)
    def funcaptcha():
        apikey = "d9dd3bdb07074dea9ff2479374632ec5"
        client = OneStCaptchaClient(apikey=apikey)
        site_key = "B7D8911C-5CC8-A9A3-35B0-554ACEE604DA"
        site_url = "https://signup.live.com/"
        while True:
            result = client.fun_captcha_task_proxyless(site_url  , site_key)
            if result["code"] == 0:  # success:
                return result["token"]
            else:  # wrong
                continue
    print(f'[{bot_number}] Solving FunCaptcha...')
    time.sleep(5)
    # wait for the fun captcha iframe with id ='enforcementFrame'
    iframe = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe#enforcementFrame'))
    )
    driver.switch_to.frame(iframe)
    time.sleep(0.5)
    token = funcaptcha()
    driver.execute_script(
    'parent.postMessage(JSON.stringify({eventId:"challenge-complete",payload:{sessionToken:"' + token + '"}}),"*")')
    print(f'[{bot_number}] FunCaptcha Solved')
    

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    done = False
    tries = 0
    # index = int(sys.argv[1])
    index = 8
    batch_size = 1
    # batch_size = int(sys.argv[2])
    while True:
        if tries > 2:
            print(f'[{bot_number}] Issue with this bot.')
            print(f'[{bot_number}] Max Tries Reached. Exiting...')
            print(f'[{bot_number}] Process Ended')
            break
        try:
            cycle_number = index + 1
            bot_number = (cycle_number % batch_size) + 1
            print(f'[{bot_number}] Starting Bot...')
            with open('names.txt', 'r') as f:
                names = f.read().splitlines()
            
            first_name = names[random.randint(0, len(names)-1)]
            last_name = names[random.randint(0, len(names)-1)]
            
            username = first_name.lower() + "_" + last_name.lower() + "_" + str(random.randint(1432, 863549))
            print(f'[{bot_number}] Username: {username}@outlook.com')
            # create strong password with max length of 10 except commas
            password = ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+=-') for i in range(10))
            print(f'[{bot_number}] Password: {password}')
            with open('ipv4.txt', 'r') as f:
                proxies = f.read().splitlines()
                proxy = proxies[index]
                proxy_host, proxy_port, proxy_username, proxy_password = proxy.split(':')
            
            print(f'[{bot_number}] Using Proxy: {proxy}')
            
            
            # create a new chrome session and destroy until there is no tunnel connection error
            proxy_tries = 0
            while True:
                if proxy_tries > 3:
                    print(f'[{bot_number}] Error Proxy Connection. Max Tries Reached. Exiting...')
                    print(f'[{bot_number}] Process Ended')
                    sys.exit()
                try:
                    driver = create_driver_with_proxy(proxy_host, proxy_port, proxy_username, proxy_password)
                    driver.get('https://signup.live.com/')
                    break
                except:
                    print(f'[{bot_number}] Error Proxy Connection. Trying Again.')
                    if driver:
                        driver.quit()
                    proxy_tries +=1
                    continue  
                
            print(f"[{bot_number}] Process Started")
            time.sleep(2)
            # wait for an anchor with id="liveSwitch"
            get_new_email_anchor = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a#liveSwitch'))
            )
            get_new_email_anchor.click()
            time.sleep(2)
            print(f'[{bot_number}] Sending Username...')
            # get input with id="MemberName"
            newemail_input = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input#MemberName'))
            )
            newemail_input.send_keys(username)
            # 
            # 
            # 
            # Reserved for changing email domain!!!!!
            # 
            # 
            # 
            # 
            
            # click on button with id="iSignupAction"
            next_button = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input#iSignupAction'))
            )
            next_button.click()
            time.sleep(2)
            print(f'[{bot_number}] Sending Password...')
            # get input with id="PasswordInput"
            password_input = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input#PasswordInput'))
            )
            password_input.send_keys(password)
            
            # click on button with id="iSignupAction"
            next_button = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input#iSignupAction'))
            )
            print(f'[{bot_number}] Full Name = {first_name} {last_name}')
            next_button.click()
            time.sleep(2)
            print(f"[{bot_number}] Sending Full Name...")
            # get input with id="FirstName"
            firstname_input = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input#FirstName'))
            )
            firstname_input.send_keys(first_name)
            # get input with id="LastName"
            lastname_input = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input#LastName'))
            )
            lastname_input.send_keys(last_name)
            
            # click on button with id="iSignupAction"
            next_button = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input#iSignupAction'))
            )
            next_button.click()
            time.sleep(2)
            print(f'[{bot_number}] Sending Aditional Info')
            # get dropdown with class="datepart0 form-control win-dropdown" and select a random value
            datepart0_dropdown = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'select.datepart0.form-control.win-dropdown'))
            )
            datepart0_dropdown.click()
            for i in range(random.randint(1, 11)):
                datepart0_dropdown.send_keys(Keys.ARROW_DOWN)
                time.sleep(0.2)
            datepart0_dropdown.send_keys(Keys.ENTER)
            
            # get dropdown with class="datepart1 form-control win-dropdown" and select a random value
            datepart1_dropdown = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'select.datepart1.form-control.win-dropdown'))
            )
            datepart1_dropdown.click()
            for i in range(random.randint(1, 28)):
                datepart1_dropdown.send_keys(Keys.ARROW_DOWN)
                time.sleep(0.2)
            datepart1_dropdown.send_keys(Keys.ENTER)
            
            # get input with id="BirthYear"
            birthyear_input = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input#BirthYear'))
            )
            birthyear_input.send_keys(random.randint(1965, 2003))
            
            # click on button with id="iSignupAction"
            next_button = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input#iSignupAction'))
            )
            next_button.click()
            solve_funcaptcha(driver)
            time.sleep(20)
            print(f'[{bot_number}] Setting Account...')
            driver.switch_to.default_content()
            # get all the buttons on page
            buttons = WebDriverWait(driver, 60).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button'))
            )
            time.sleep(2)
            print(f'[{bot_number}] Agreeing to Terms...')
            while True:
                buttons[0].click()
                time.sleep(10)
                url = driver.current_url
                if 'privacynotice' in url:
                    continue
                else:
                    done = True
                    break
            
            if done:
                break
            else:
                driver.quit()
                tries +=1
                continue
        except Exception as e:
            print(f'[{bot_number}] Error with process. Trying Again.')
            driver.quit()
            tries +=1
            continue
        
    if done:    
        print(f'[{bot_number}] Account Ready to Use')  
        # check the account file
        account_file = os.path.join(base_dir,'assets', 'outlook_mails.csv')
        if not os.path.isfile(account_file):
            with open(account_file, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(['status','username', 'password'])
        
        with open(account_file, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(['none',f"{username}@outlook.com", password])
        print(f'[{bot_number}] Account Saved')
        
        try :
            print(f'[{bot_number}] Going to Inbox...')
            driver.get('https://outlook.office.com/owa/')
            time.sleep(5)
            
            print(f'[{bot_number}] Initiating Inbox...')
            # get input with id="i0116"
            inbox_input = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input#i0116'))
            )
            inbox_input.send_keys(f"{username}@outlook.com")
            inbox_input.send_keys(Keys.ENTER)
            tries = 0
            while True:
                if tries > 4:
                    print(f'[{bot_number}] Inbox Initiation Failed. "Timeout Error"')
                    break
                time.sleep(15)
                url = driver.current_url
                if '/0/' in url:
                    time.sleep(20)
                    driver.save_screenshot(f'inbox{random.randint(0,100000)}.png')
                    print(f'[{bot_number}] Inbox Ready')
                    break
                else:
                    tries +=1
                    continue
            
            print(f'[{bot_number}] Process Ended')
        except Exception as e:
            randon_number = random.randint(1, 10000)
            driver.save_screenshot(f'error{randon_number}.png')
            print(f'[{bot_number}] Issue contacting Inbox. But Account is ready.')
            print(f'[{bot_number}] Issue Snapshot Saved as error{randon_number}.png')
            print(f'[{bot_number}] Process Ended')
    driver.quit()
