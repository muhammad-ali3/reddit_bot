from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
import random
def create_driver_with_proxy(proxy_host, proxy_port, proxy_username, proxy_password, is_profile=False):
    if is_profile:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        profiles_dir = os.path.join(base_dir,'assets','profiles')
        profile_name = "".join([random.choice('abcdefghijklmnopqrstuvwxyz0123456789_') for i in range(20)])
        profile_dir = os.path.join(profiles_dir, profile_name)
        if not os.path.exists(profiles_dir):
            os.makedirs(profiles_dir)
        if not os.path.exists(profile_dir):
            os.makedirs(profile_dir)
        
        
    # Set up Selenium-Wire options for the proxy
    proxy_options = {
        'proxy': {
            'http': f'http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}',
            'https': f'https://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}',
            'no_proxy': 'localhost,127.0.0.1',  # Add any addresses you don't want to proxy
        }
    }
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--log-level=3')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-extensions")
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    
    # set user data dir
    if is_profile:
        options.add_argument(f'--user-data-dir={profile_dir}')
        
    # Set up the Chrome driver with the proxy options
    driver = webdriver.Chrome(options=options, seleniumwire_options=proxy_options)
    if is_profile:
        return driver, profile_dir
    else:
        return driver