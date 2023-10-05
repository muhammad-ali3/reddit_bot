# Description: This file contains the function to get the proxies from the a file
import os
import csv

def get_proxies():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fresh_proxies = os.path.join(base_dir,'assets', 'fresh_proxies.txt')
    proxies = []
    with open(fresh_proxies, 'r') as f:
        lines = f.readlines()
        for row in lines:
            row = row.strip()
            proxies.append(row)
    # Return the proxies
    return proxies               
    
    