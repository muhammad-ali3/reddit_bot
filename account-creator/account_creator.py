import os
import csv
import time
import random
import sys
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from driver import create_driver_with_proxy
from proxy import get_proxies
from first_captcha import ReCapthca
import shutil
import re
from bs4 import BeautifulSoup
import essentials
from outlook import Reddit_Verify

def signup_process(email, driver):
    # Get current time in seconds
    current_time = time.time()
    driver.get('https://www.reddit.com/account/register')
    # wait until page loads
    time.sleep(5)
    print(f'[{bot_number}] Using Email: {email}.')
    print(f'[{bot_number}] Starting Signup')
    # get input field with id="regEmail"
    email_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'regEmail'))
    )
    email_field.send_keys(email)
    # get submit button with text="Continue"
    email_field.submit()

    # WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.OnboardingStep[data-step="username-and-password"]')))
    # get all anchors with class="Onboarding__usernameSuggestion"
    usernames = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.XPATH, '//a[contains(@class, "Onboarding__usernameSuggestion")]'))
    )
    # click on a random username
    random_username_selected = usernames[random.randint(0, len(usernames) - 1)]
    username = random_username_selected.get_attribute('data-username')
    random_username_selected.click()
    # get input field with id="regPassword"
    password_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'regPassword'))
    )
    # get strong password of length 10 except comma in it
    password = ''.join ([random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+') for i in range(10)])
    password_field.send_keys(password)
    # get form content with class="AnimatedForm__content"
    form_content = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'AnimatedForm__content'))
    )
    form_content.click()
    # get iframe with title="reCAPTCHA"
    iframe = WebDriverWait(driver, 60).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'iframe[title="reCAPTCHA"]'))
    )
    driver.switch_to.frame(iframe)
    # get div with id="rc-anchor-container"
    recaptcha_container = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'rc-anchor-container'))
    )
    
    driver.switch_to.default_content()
    print(f'[{bot_number}] Solving Captcha')
    # create captcha task
    task_id = ReCapthca.crate_task()
    result = ReCapthca.get_results(task_id)
    print(f'[{bot_number}] Response Recieved From 1stCaptcha')
    if result is not False:
        driver.execute_script(
            f'document.getElementById("g-recaptcha-response").innerHTML = "{result}"'
        )
        print(f'[{bot_number}] Captcha ByPassed')
        # get submit button with class="AnimatedForm__submitButton SignupButton"
        sign_up_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.AnimatedForm__submitButton.SignupButton'))
        )
        sign_up_button.click()
    else:
        print(f'[{bot_number}] Error with Captcha Solving, Captcha Service Trowed Error')

    time.sleep(10)
    if '/account/register/' not in driver.current_url:
        return [True, current_time, email, username, password]
    else:
        print(f'[{bot_number}] Ip/proxy blocked by the site, Signup blocked Trying Again')
        return [False, None, None, None, None]
    
def verify_mail(driver, user, passw):
    time.sleep(30)
    mail_res = Reddit_Verify.outlook_mail(bot_number, user, passw)
    if not mail_res:
        return False
    else:
        driver.get(mail_res)
        time.sleep(5)
        return True

def calibrate_setting_process(driver):
    driver.get('https://www.reddit.com/settings/feed/')
    time.sleep(5)
    agree_for_cookies()
    # get all buttons with attribute 'aria-checked'
    buttons = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'button[aria-checked]'))
    )
    # Analyze and find id of required toggles to interact
    adult_toggle = buttons[0]
    # Finds Safe Search toggle on page
    safe_toggle = buttons[1]
    # Finds Community Theme toggle on page
    theme_toggle = buttons[5]


    # Get the toggle status of required toggles (true/on) and (false/off)
    def get_adult_value():
        return adult_toggle.get_attribute('aria-checked')
    def get_safe_value():
        return safe_toggle.get_attribute('aria-checked')
    def get_theme_value():
        return theme_toggle.get_attribute('aria-checked')

    # Calibrate Feed settings according to requirements
    # Defining sub-functions to verify desired settings
    def check_adult_toggle():
        while True:
            adult_toggle_value = get_adult_value()
            if adult_toggle_value != 'true':
                adult_toggle.click()
                print(f'[{bot_number}] Adult Content Toggle Enabled')
                break
            else:
                continue
    def check_safe_toggle():
        while True:
            safe_toggle_value = get_safe_value()
            if safe_toggle_value == 'true':
                safe_toggle.click()
                print(f'[{bot_number}] Safe Search Toggle Disabled')
                break
            else:
                continue
    def check_theme_toggle():
        while True:
            theme_toggle_value = get_theme_value()
            if theme_toggle_value == 'true':
                theme_toggle.click()
                print(f'[{bot_number}] Community Theme Toggle Disabled')
                break
            else:
                continue
            
    check_adult_toggle()
    check_safe_toggle()
    check_theme_toggle()
    return True

def randomize_avatar(driver):
    driver.get('https://www.reddit.com/avatar/explore')
    time.sleep(5)
    agree_for_cookies()
    randomize_button = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(@data-testid, 'actions:randomize')]"))
    )
    # Click the button
    randomize_button.click()
    time.sleep(5)
    save_button = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(@data-testid, 'actions:save')]"))
    )
    # Click the button
    save_button.click()
    time.sleep(5)
    return True


def agree_for_cookies():
    print(f'[{bot_number}] Checking for Cookies Banner on this Page.')
    try:
        cookies_alert = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@style,"opacity: 1; x: 1px; y: 0px; transform: translateY(0px) scale(1, 1); --Toaster-indicatorColor: #24A0ED;")]'))
        )
        html = cookies_alert.get_attribute("innerHTML")
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Find the first button element
        first_button = soup.find('button')

        if first_button:
            # Get the class attribute of the first button
            button_class_list = first_button.get('class')

            # Combine the classes into a single string
            button_class_string = ' '.join(button_class_list)

            accept_button_class = button_class_string
        accept_button = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, f'//button[contains(concat(" ", @class), " {accept_button_class} ")]'))
        )
        accept_button[0].click()
        print(f'[{bot_number}] Cookies Aleart Accepted.')
    except:
        print(f"[{bot_number}] No Cookies Aleart Found on this Page.")
        

        

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    save_file = False
    index = int(sys.argv[1])
    # index = 9
    batch_size = int(sys.argv[2])
    # batch_size = 1
    cycle_number = index + 1
    bot_number = (cycle_number % batch_size) + 1
    assets_dir = os.path.join(base_dir, 'assets')
    proxies_file = os.path.join(assets_dir, 'fresh_proxies.txt')
    generated_mails_file = os.path.join(assets_dir, 'fresh_outlook_mails.txt')
    proxies = get_proxies()
    proxy = proxies[index]
    proxy_host, proxy_port, proxy_username, proxy_password = proxy.split(':')
    
    # open generated_csv file and igniore the first line
    with open(generated_mails_file, 'r') as file:
        mails = []
        lines = file.readlines()
        for row in lines:
            row = row.strip()
            mails.append(row)
    email = mails[index]
    email_password = essentials.get_password(email)
    
    print(f'[{bot_number}] Starting Bot.')
    print(f'[{bot_number}] Selected Proxy: {proxy_username}.')
    
    tries = 0
    while True:
        if tries > 2:
            print(f'[{bot_number}] Tried 2 times, but failed to get a valid proxy connection.')
            essentials.change_status('proxy', proxy, 'error')
            sys.exit(0)
        try:
            # create a new chrome session
            driver, profile_name = create_driver_with_proxy(proxy_host, proxy_port, proxy_username, proxy_password, is_profile=True)
            driver.get('https://www.reddit.com/account/register')
            time.sleep(5)
            break
        except:
            print(f'[{bot_number}] Error Connecting Proxy, Trying Again')
            driver.quit()
            tries += 1
            continue
    
    try: 
        response = signup_process(email, driver)
        if response[0] == True:
            print(f'[{bot_number}] Signup Successfull')
            print(f'[{bot_number}] Email: {response[2]}')
            print(f'[{bot_number}] Email Password: {email_password}')
            print(f'[{bot_number}] Username: {response[3]}')
            print(f'[{bot_number}] Password: {response[4]}')
            print(f'[{bot_number}] Time Taken: {int(time.time() - response[1])} seconds')
            save_file = True
            # get date and time in DD-MM-YYYT HH:MM:SS format
            date_time = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(response[1]))
            file_text = f'{response[3]},{response[4]},{response[2]},{proxy_username},{date_time},General,General'
            calibrate = False
            avatar = False
            try:
                print(f'[{bot_number}] Calibrating Settings')
                res = calibrate_setting_process(driver)
                if res == True:
                    print(f'[{bot_number}] Settings Calibrated')
                    calibrate = True
                else:
                    print(f'[{bot_number}] Error Calibrating Settings')
                    calibrate = False
            except:
                print(f'[{bot_number}] Error Calibrating Settings')
                calibrate = False
            try:
                print(f'[{bot_number}] Randomizing Avatar')
                res = randomize_avatar(driver)
                if res == True:
                    print(f'[{bot_number}] Avatar Randomized')
                    avatar = True
                else:
                    print(f'[{bot_number}] Error Randomizing Avatar')
                    avatar = False
            except:
                print(f'[{bot_number}] Error Randomizing Avatar')
                avatar = False
            
            try:
                print(f'[{bot_number}] Verifying Mail')
                res = verify_mail(driver, response[2], email_password)
                if res == True:
                    print(f'[{bot_number}] Mail Verified')
                    file_text += ',1'
                else:
                    print(f'[{bot_number}] Error Verifying Mail')
                    file_text += ',0'
            except Exception as e:
                print(f'[{bot_number}] Error Verifying Mail: {e}')
                file_text += ',0'
                
            if calibrate == True and avatar == True:
                print(f'[{bot_number}] Account Ready to Use')
                file_text += ',1'
            else:
                print(f'[{bot_number}] Some Steps Failed')
                file_text += ',0'
        else:
            print(f'[{bot_number}] Signup Failed')
    except Exception as e:
        print(f'[{bot_number}] Error: {e}')
    
    if save_file == True:
        accounts_file = os.path.join(base_dir,'assets', 'accounts.csv')
        if os.path.exists(accounts_file) == False:
            header = 'username,password,email,proxy,date_created,primary_role,secondary_role,is_verified,is_setup,last_karma_post,last_shadowban_check\n'
            with open(accounts_file, 'w') as file:
                file.write(header)
        file_text += ',,\n'
        with open(accounts_file, 'a') as file:
            file.write(file_text)
        print(f'[{bot_number}] Account created.')
        essentials.change_status('mail', response[2], 'used')
        essentials.change_status('proxy', proxy, 'used')
    else:
        print(f'[{bot_number}] Nothing to Save in File')
    
    if save_file == True:
        import pickle
        # Save cookies in pkl file
        cookies_dir = os.path.join(base_dir,'assets','cookies')
        if os.path.isdir(cookies_dir) == False:
            os.mkdir(cookies_dir)
        cookies = driver.get_cookies()
        file_name = f'{response[3]}.pkl'
        file_path = os.path.join(cookies_dir, file_name)
        with open(file_path, 'wb') as filehandler:
            pickle.dump(cookies, filehandler)
        print(f'[{bot_number}] Cookies Saved')
        
    driver.quit()
    
    profiles_dir = os.path.join(base_dir,'assets','profiles')
    profile_dir = os.path.join(profiles_dir, profile_name)
    if save_file == True:
        # rename profile dir
        os.rename(profile_dir, os.path.join(profiles_dir, response[3]))
        print(f'[{bot_number}] Profile Saved')
    else:
        # remove profile non empty dir
        shutil.rmtree(profile_dir)
    
    print(f'[{bot_number}] Bot Finished')
    
