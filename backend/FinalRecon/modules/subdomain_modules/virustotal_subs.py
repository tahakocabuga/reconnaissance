#!/usr/bin/env python3

R = '\033[31m'  # red
G = '\033[32m'  # green
C = '\033[36m'  # cyan
W = '\033[0m'   # white
Y = '\033[33m'  # yellow

from json import loads
import modules.subdom as parent


async def virust(hostname, conf_path, session):
	with open(f'{conf_path}/keys.json', 'r') as keyfile:
		json_read = keyfile.read()

	json_load = loads(json_read)
	vt_key = json_load['virustotal']

	if vt_key is not None:
		print(f'[!] Requesting VirusTotal')
		url = f'https://www.virustotal.com/api/v3/domains/{hostname}/subdomains'
		vt_headers = {
			'x-apikey': vt_key
		}
		try:
			async with session.get(url, headers=vt_headers) as resp:
				sc = resp.status
				if sc == 200:
					json_data = await resp.text()
					json_read = loads(json_data)
					domains = json_read['data']
					tmp_list = []
					for i in range(0, len(domains)):
						tmp_list.append(domains[i]['id'])
					print(f'[+] VirusTotal found {len(tmp_list)} subdomains!')
					parent.found.extend(tmp_list)
				else:
					print(f'[-] VirusTotal Status : {sc}')
		except Exception as e:
			print(f'[-] VirusTotal Exception : {e}')
	else:
		print(f'[!] Skipping VirusTotal : API key not found!')
