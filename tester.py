# selenium wire code to create driver with proxy
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options

proxy = '173.211.8.56:6168:zjtzrhbn:x047kltc9qoy'
proxy_host, proxy_port, proxy_username, proxy_password = proxy.split(':')
# set proxy
chrome_options = Options()
proxy_options = {
    'proxy': {
        'http': f'http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}',
        'https': f'https://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}',
        'no_proxy': 'localhost', # Add any addresses you don't want to proxy
    }
}
driver = webdriver.Chrome(options=chrome_options, seleniumwire_options=proxy_options)
driver.get('https://www.reddit.com')
input('Press enter to quit')