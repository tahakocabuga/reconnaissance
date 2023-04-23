#!/usr/bin/env python3

R = '\033[31m'  # red
G = '\033[32m'  # green
C = '\033[36m'  # cyan
W = '\033[0m'   # white
Y = '\033[33m'  # yellow

from json import loads
import modules.subdom as parent


async def certspot(hostname, session):
	print(f'[!] Requesting CertSpotter')
	url = 'https://api.certspotter.com/v1/issuances'
	cs_params = {
		'domain': hostname,
		'expand': 'dns_names',
		'include_subdomains': 'true'
	}

	try:
		async with session.get(url, params=cs_params) as resp:
			sc = resp.status
			if sc == 200:
				json_data = await resp.text()
				json_read = loads(json_data)
				print(f'[+] Certsport found {len(json_read)} subdomains!')
				for i in range(0, len(json_read)):
					domains = json_read[i]['dns_names']
					parent.found.extend(domains)
			else:
				print(f'[-] CertSpotter Status : {sc}')
	except Exception as e:
		print(f'[-] CertSpotter Exception : {e}')
