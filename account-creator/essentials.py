import pandas as pd
import requests
import os

def change_status(hint, identifier, status):
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    mail_path = os.path.join(base_dir, 'assets', 'outlook_mails.csv')
    proxy_path = os.path.join(base_dir, 'assets', 'proxies.csv')
    if 'mail' in hint.lower():
        df = pd.read_csv(mail_path)
        for index, row in df.iterrows():
            if identifier in row['username']:
                df.loc[index, 'status'] = status
                df.to_csv(mail_path, index=False)
                return True
        return False
    if 'prox' in hint.lower():
        df = pd.read_csv(proxy_path)
        for index, row in df.iterrows():
            if identifier in row['proxy']:
                df.loc[index, 'status'] = status
                df.to_csv(proxy_path, index=False)
                return True
        return False
    
def get_password(username):
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    outlook_path = os.path.join(base_dir, 'assets', 'outlook_mails.csv')
    df = pd.read_csv(outlook_path)
    for index, row in df.iterrows():
        if username in row['username']:
            return row['password']

def get_proxy(identifier):
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    proxies_path = os.path.join(base_dir, 'assets', 'proxies.csv')
    df = pd.read_csv(proxies_path)
    for index, row in df.iterrows():
        if identifier in row['proxy']:
            return row['proxy']
    return False

def get_country_info(cca2):
    country = False
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    countries_path = os.path.join(base_dir, 'assets', 'countries.csv')
    df = pd.read_csv(countries_path)
    for index, row in df.iterrows():
        if row['CCA2'] == cca2:
            country = row['Name']
            break
        continue
    while True:
        try:
            response = requests.get(f'https://countryinfoapi.com/api/countries/name/{country}')
            break
        except:
            continue
    timezone = response.json()['timezones'][0]
    language = response.json()['languages']
    # get value of first key in dict
    language = list(language.keys())[0]
    return timezone, language
    
    