#!/usr/bin/env python3

R = '\033[31m'  # red
G = '\033[32m'  # green
C = '\033[36m'  # cyan
W = '\033[0m'   # white
Y = '\033[33m'  # yellow

from json import loads
import modules.subdom as parent


async def anubisdb(hostname, session):
	print(f'[!] Requesting AnubisDB')
	url = f'https://jldc.me/anubis/subdomains/{hostname}'
	try:
		async with session.get(url) as resp:
			sc = resp.status
			if sc == 200:
				output = await resp.text()
				json_out = loads(output)
				parent.found.extend(json_out)
				print(f'[+] AnubisDB found {len(json_out)} subdomains!')
			elif sc == 300:
				pass
			else:
				print(f'[-] AnubisDB Status : {sc}')
	except Exception as e:
		print(f'[-] AnubisDB Exception : {e}')
