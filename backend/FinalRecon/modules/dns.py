#!/usr/bin/env python3

import dnslib
from modules.export import export

R = '\033[31m'  # red
G = '\033[32m'  # green
C = '\033[36m'  # cyan
W = '\033[0m'   # white
Y = '\033[33m'  # yellow


def dnsrec(domain, output, data):
	result = {}
	print(f'\n[!] Starting DNS Enumeration...\n')
	types = ['A', 'AAAA', 'ANY', 'CAA', 'CNAME', 'MX', 'NS', 'TXT']
	full_ans = []
	for Type in types:
		q = dnslib.DNSRecord.question(domain, Type)
		pkt = q.send('8.8.8.8', 53, tcp='UDP')
		ans = dnslib.DNSRecord.parse(pkt)
		ans = str(ans)
		ans = ans.split('\n')
		full_ans.extend(ans)
	full_ans = set(full_ans)
	dns_found = []

	for entry in full_ans:
		if entry.startswith(';') is False:
			dns_found.append(entry)
		else:
			pass

	if len(dns_found) != 0:
		for entry in dns_found:
			print(f'{entry}')
			if output != 'None':
				result.setdefault('dns', []).append(entry)
	else:
		print(f'[-] DNS Records Not Found!')
		if output != 'None':
			result.setdefault('dns', ['DNS Records Not Found'])

	dmarc_target = f'_dmarc.{domain}'
	q = dnslib.DNSRecord.question(dmarc_target, 'TXT')
	pkt = q.send('8.8.8.8', 53, tcp='UDP')
	dmarc_ans = dnslib.DNSRecord.parse(pkt)
	dmarc_ans = str(dmarc_ans)
	dmarc_ans = dmarc_ans.split('\n')
	dmarc_found = []

	for entry in dmarc_ans:
		if entry.startswith('_dmarc') is True:
			dmarc_found.append(entry)
		else:
			pass
	if len(dmarc_found) != 0:
		for entry in dmarc_found:
			print(f'{entry}')
			if output != 'None':
				result.setdefault('dmarc', []).append(entry)
	else:
		print(f'\n[-] DMARC Record Not Found!')
		if output != 'None':
			result.setdefault('dmarc', ['DMARC Record Not Found!'])
	result.update({'exported': False})

	if output != 'None':
		data['module-DNS Enumeration'] = result
		fname = f'{output["directory"]}/dns_records.{output["format"]}'
		output['file'] = fname
		export(output, data)
