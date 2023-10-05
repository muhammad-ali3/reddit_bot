from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def check_mail(driver, user, passw):
    # get input with name="loginfmt"
    email_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "loginfmt"))
    )
    email_field.send_keys(user)
    email_field.send_keys(Keys.ENTER)
    time.sleep(5)
    password_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "i0118"))
    )
    password_field.send_keys(passw)
    password_field.send_keys(Keys.ENTER)
    time.sleep(5)
    res = check_blocked(driver)
    if res == True:
        return False
    time.sleep(5)
    url = driver.current_url
    if 'ppsecure' in  url:
        # find input with id="KmsiCheckboxField"
        kmsi_checkbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "KmsiCheckboxField"))
        )
        kmsi_checkbox.send_keys(Keys.ENTER)
        time.sleep(30)
        url = driver.current_url
        if '/mail/url/0/' in url:
            print('Sign in Successful')
            return True
        
    
def check_blocked(driver):
    url = driver.current_url
    if 'Abuse' in  url:
        print('Blocked')
        return True
    else:
        print('Not Blocked')
        return False


    
    


    