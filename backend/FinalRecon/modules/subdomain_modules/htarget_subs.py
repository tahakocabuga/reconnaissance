#!/usr/bin/env python3

R = '\033[31m'  # red
G = '\033[32m'  # green
C = '\033[36m'  # cyan
W = '\033[0m'   # white
Y = '\033[33m'  # yellow

import modules.subdom as parent


async def hackertgt(hostname, session):
	print(f'[!] Requesting HackerTarget')
	url = f'https://api.hackertarget.com/hostsearch/?q={hostname}'
	try:
		async with session.get(url) as resp:
			sc = resp.status
			if sc == 200:
				data = await resp.text()
				data_list = data.split('\n')
				tmp_list = []
				for line in data_list:
					subdomain = line.split(',')[0]
					tmp_list.append(subdomain)
				print(f'[+] HackerTarget found {len(tmp_list)} subdomains!')
				parent.found.extend(tmp_list)
			else:
				print(f'[-] HackerTarget Status : {sc}')
	except Exception as e:
		print(f'[-] HackerTarget Exception : {e}')
