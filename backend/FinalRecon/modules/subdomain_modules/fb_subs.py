#!/usr/bin/env python3

R = '\033[31m'  # red
G = '\033[32m'  # green
C = '\033[36m'  # cyan
W = '\033[0m'   # white
Y = '\033[33m'  # yellow

from json import loads
import modules.subdom as parent


async def fb_cert(hostname, conf_path, session):
	with open(f'{conf_path}/keys.json', 'r') as keyfile:
		json_read = keyfile.read()

	json_load = loads(json_read)
	fb_key = json_load['facebook']

	if fb_key is not None:
		print(f'[!] Requesting Facebook')
		url = 'https://graph.facebook.com/certificates'
		fb_params = {
			'query': hostname,
			'fields': 'domains',
			'access_token': fb_key
		}
		try:
			async with session.get(url, params=fb_params) as resp:
				sc = resp.status
				if sc == 200:
					json_data = await resp.text()
					json_read = loads(json_data)
					domains = json_read['data']
					print(f'[+] Facebook found {len(domains)} subdomains!')
					for i in range(0, len(domains)):
						parent.found.extend(json_read['data'][i]['domains'])
				else:
					print(f'[-] Facebook Status : {sc}')
		except Exception as e:
			print(f'[-] Facebook Exception : {e}')
	else:
		print(f'[!] Skipping Facebook : API key not found!')
