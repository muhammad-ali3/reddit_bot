from proxy import get_proxies
import os
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fresh_proxies = os.path.join(base_dir,'assets', 'fresh_proxies.txt')
proxies = get_proxies(fresh_proxies)
for index , row in enumerate(proxies):
    print(index + 1,':', row)