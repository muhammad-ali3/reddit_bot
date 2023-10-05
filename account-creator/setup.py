import os
import csv

if __name__ == "__main__":
    # create assets directory
    assets_dir = os.path.join(os.getcwd(), 'assets')
    if not os.path.exists(assets_dir):
        os.mkdir(assets_dir)
    # create proxies file
    proxies_file = os.path.join(assets_dir, 'proxies.txt')
    if not os.path.exists(proxies_file):
        with open(proxies_file, 'w') as file:
            file.write('username,password,email,proxy_identifier,date_created,primary_role,secondary_role,is_verified,is_setup,last_karma_post,last_shadowban_check')
            file.close()
    # create generated_mails file
    generated_mails_file = os.path.join(assets_dir, 'generated_mails.csv')
    if not os.path.exists(generated_mails_file):
        with open(generated_mails_file, 'w') as file:
            file.write('email,apple_id')
            file.close()
    # check outlook_mails file
    outlook_mails_file = os.path.join(assets_dir, 'outlook_mails.txt')
    if not os.path.exists(outlook_mails_file):
        with open(outlook_mails_file, 'w') as file:
            file.write('email,password')
            file.close()
    
    