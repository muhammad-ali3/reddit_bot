from selenium import webdriver
from selenium_authenticated_proxy import SeleniumAuthenticatedProxy
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize Chrome options
chrome_options = webdriver.ChromeOptions()

# Initialize SeleniumAuthenticatedProxy
proxy_helper = SeleniumAuthenticatedProxy(proxy_url="http://lucrumfansagencyftS-country-UK-city-Glasgow-session-c7s9crom-ttl-36000000000:nnrYhBU9@resi.ipv6.plainproxies.com:8080")

# Enrich Chrome options with proxy authentication
proxy_helper.enrich_chrome_options(chrome_options)

# Start WebDriver with enriched options
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://signup.live.com/')
time.sleep(200)
def enter_credentials(driver, user, passw):
    # get input with name="loginfmt"
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "loginfmt"))
    )
    email_field.send_keys(user)
    # press Enter
    email_field.send_keys(Keys.ENTER)
    time.sleep(10)
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "i0118"))
    )
    password_field.send_keys(passw)
    password_field.send_keys(Keys.ENTER)
    time.sleep(10)

username = "willeke_rammel_404919@outlook.com"
password = "yRJS)ag6h)"
enter_credentials(driver, username, password)