#!/usr/bin/env python3

R = '\033[31m'  # red
G = '\033[32m'  # green
C = '\033[36m'  # cyan
W = '\033[0m'   # white
Y = '\033[33m'  # yellow

from json import loads
import modules.subdom as parent


async def sonar(hostname, session):
	print(f'[!] Requesting Sonar')
	url = f'https://sonar.omnisint.io/subdomains/{hostname}'
	try:
		async with session.get(url) as resp:
			sc = resp.status
			if sc == 200:
				json_data = await resp.text()
				json_read = loads(json_data)
				print(f'[+] Sonar found {len(json_read)} subdomains!')
				parent.found.extend(json_read)
			else:
				print(f'[-] Sonar Status : {sc}')
	except Exception as e:
		print(f'[-] Sonar Exception : {e}')
