import os
import sys
import pandas as pd

if __name__ == "__main__":
    action = str(sys.argv[1])
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    proxies_path = os.path.join(base_dir, 'assets', 'proxies.csv')
    fresh_proxies_path = os.path.join(base_dir,'assets','fresh_proxies.txt')
    outlook_path = os.path.join(base_dir, 'assets', 'outlook_mails.csv')
    fresh_outlook_path = os.path.join(base_dir, 'assets', 'fresh_outlook_mails.txt')
    if 'update' in action:
        csv = pd.read_csv(proxies_path)
        proxies = []
        for index, row in csv.iterrows():
            if row['status'] == 'none':
                proxies.append(f"{row['proxy']}\n")

        with open(fresh_proxies_path, 'w') as file:
            file.writelines(proxies)
        
        csv = pd.read_csv(outlook_path)
        outlooks = []
        for index, row in csv.iterrows():
            if row['status'] == 'none':
                outlooks.append(f"{row['username']}\n")
        
        with open(fresh_outlook_path, 'w') as file:
            file.writelines(outlooks)
    
    elif 'add' in action:
        new_proxies_path = os.path.join(base_dir,'account-creator', 'ipv6.txt')             
        destination_path = os.path.join(base_dir, 'assets', 'proxies.csv')
        new_proxies = []
        with open(new_proxies_path, 'r') as file:
            new_proxies = [line.strip() for line in file.readlines() if line.strip()]
            
            if len(new_proxies) == 0:
                pass
            else:
                with open(destination_path, 'a') as f:
                    for proxy in new_proxies:
                        f.write(f"none,{proxy}\n")
                print('New proxies added to the list')
        with open(new_proxies_path, 'w') as file:
            file.write('')
            
        # copy ipv4  proxies
        ipv4_proxies_path = os.path.join(base_dir,'outlook-creator', 'ipv4.txt')
        des_path = os.path.join(base_dir, 'assets', 'ipv4.txt')
        with open(ipv4_proxies_path, 'r') as file:
            ipv4_proxies = [line.strip() for line in file.readlines() if line.strip()]
            if len(ipv4_proxies) == 0:
                pass
            else:
                with open(des_path, 'a') as f:
                    for proxy in ipv4_proxies:
                        f.write(f"{proxy}\n")
            
        print('Proceeding.....')
        
    elif 'clear' in action:
        if 'prox' in action:
            #  remove all proxies in the csv file
            csv = pd.read_csv(proxies_path)
            # remove all emails with status none except the header
            csv = csv[csv['status'] != 'none']
            csv.to_csv(proxies_path, index=False)
            print('All proxies cleared')
        elif 'mail' in action:
            # remove all outlooks with status none except the header
            csv = pd.read_csv(outlook_path)
            csv = csv[csv['status'] != 'none']
            csv.to_csv(outlook_path, index=False)
            print('All outlooks cleared')
        else:
            print('Please Specify what to clear')
        
                