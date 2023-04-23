#!/usr/bin/env python3

R = '\033[31m'  # red
G = '\033[32m'  # green
C = '\033[36m'  # cyan
W = '\033[0m'   # white
Y = '\033[33m'  # yellow

from json import loads
import modules.subdom as parent

async def bevigil(hostname, conf_path, session):
    with open(f'{conf_path}/keys.json', 'r') as keyfile:
        json_read = keyfile.read()

    json_load = loads(json_read)    
    bevigil_key = json_load['bevigil']

    if bevigil_key is not None:    
        print(f'[!] Requesting BeVigil')
        url = f"https://osint.bevigil.com/api/{hostname}/subdomains/"
        header = {"X-Access-Token": bevigil_key}
        
        try:
            async with session.get(url, headers=header) as resp:
                sc = resp.status
                if sc == 200:
                    json_data: list = await resp.json()
                    subdomains = json_data.get("subdomains")
                    print(f'[+] BeVigil found {len(subdomains)} subdomains!')
                    parent.found.extend(subdomains)
                else:
                    print(f'[-] BeVigil Status : {sc}')

        except Exception as e:
            print(f'[-] BeVigil Exception : {e}')
    else:
        print(f'[!] Skipping BeVigil : API key not found!')