#!/usr/bin/env python3

R = '\033[31m'  # red
G = '\033[32m'  # green
C = '\033[36m'  # cyan
W = '\033[0m'   # white
Y = '\033[33m'  # yellow

from json import loads
import modules.subdom as parent


async def shodan(hostname, conf_path, session):
	with open(f'{conf_path}/keys.json', 'r') as keyfile:
		json_read = keyfile.read()

	json_load = loads(json_read)
	sho_key = json_load['shodan']

	if sho_key is not None:
		print(f'[!] Requesting Shodan')
		url = f'https://api.shodan.io/dns/domain/{hostname}?key={sho_key}'

		try:
			async with session.get(url) as resp:
				sc = resp.status
				if sc == 200:
					json_data = await resp.text()
					json_read = loads(json_data)
					domains = json_read['subdomains']
					tmp_list = []
					for i in range(0, len(domains)):
						tmp_list.append(f'{domains[i]}.{hostname}')
					print(f'[+] Shodan found {len(tmp_list)} subdomains!')
					parent.found.extend(tmp_list)
				else:
					print(f'[-] Shodan Status : {sc}')
		except Exception as e:
			print(f'[-] Shodan Exception : {e}')
	else:
		print(f'[!] Skipping Shodan : API key not found!')
