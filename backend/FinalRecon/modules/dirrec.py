#!/usr/bin/env python3


import socket
import aiohttp
import asyncio
from datetime import date
from modules.export import export

R = '\033[31m'  # red
G = '\033[32m'  # green
C = '\033[36m'  # cyan
W = '\033[0m'   # white
Y = '\033[33m'  # yellow

header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0'}
count = 0
wm_count = 0
found = []
responses = []
curr_yr = date.today().year
last_yr = curr_yr - 1


async def fetch(url, session, redir):
	global responses
	try:
		async with session.get(url, headers=header, allow_redirects=redir) as response:
			responses.append((url, response.status))
			return response.status
	except Exception as e:
		print(f'[-] Exception : ' + str(e).strip('\n'))


async def insert(queue, filext, target, wdlist, redir):
	if len(filext) == 0:
		url = target + '/{}'
		with open(wdlist, 'r') as wordlist:
			for word in wordlist:
				word = word.strip()
				await queue.put([url.format(word), redir])
				await asyncio.sleep(0)
	else:
		filext = ',' + filext
		filext = filext.split(',')
		with open(wdlist, 'r') as wordlist:
			for word in wordlist:
				for ext in filext:
					ext = ext.strip()
					if len(ext) == 0:
						url = target + '/{}'
					else:
						url = target + '/{}.' + ext
					word = word.strip()
					await queue.put([url.format(word), redir])
					await asyncio.sleep(0)


async def consumer(queue, target, session, redir, total_num_words):
	global count
	while True:
		values = await queue.get()
		url = values[0]
		redir = values[1]
		status = await fetch(url, session, redir)
		await filter_out(target, url, status)
		queue.task_done()
		count += 1
		print(f'[!] Requests : {count}/{total_num_words}', end='\r')


async def run(target, threads, tout, wdlist, redir, sslv, dserv, filext, total_num_words):
	queue = asyncio.Queue(maxsize=threads)

	resolver = aiohttp.AsyncResolver(nameservers=dserv.split(', '))
	conn = aiohttp.TCPConnector(limit=threads, resolver=resolver, family=socket.AF_INET, verify_ssl=sslv)
	timeout = aiohttp.ClientTimeout(total=None, sock_connect=tout, sock_read=tout)
	async with aiohttp.ClientSession(connector=conn, timeout=timeout) as session:
		distrib = asyncio.create_task(insert(queue, filext, target, wdlist, redir))
		workers = [
			asyncio.create_task(
				consumer(queue, target, session, redir, total_num_words)
			) for _ in range(threads)]

		await asyncio.gather(distrib)
		await queue.join()

		for worker in workers:
			worker.cancel()


async def filter_out(target, url, status):
	global found
	if status in {200}:
		if str(url) != target + '/':
			found.append(url)
			print(f'{status} | {url}')
	elif status in {301, 302, 303, 307, 308}:
		found.append(url)
		print(f'{status} | {url}')
	elif status in {403}:
		found.append(url)
		print(f'{status} | {url}')
	else:
		pass


def dir_output(output, data):
	global responses, found
	result = {}

	for entry in responses:
		if entry is not None:
			if entry[1] in {200}:
				if output != 'None':
					result.setdefault('Status 200', []).append(f'200, {entry[0]}')
			elif entry[1] in {301, 302, 303, 307, 308}:
				if output != 'None':
					result.setdefault(f'Status {entry[1]}', []).append(f'{entry[1]}, {entry[0]}')
			elif entry[1] in {403}:
				if output != 'None':
					result.setdefault('Status 403', []).append(f'{entry[1]}, {entry[0]}')
			else:
				pass

	print(f'\n\n[+] Directories Found   : {len(found)}')

	if output != 'None':
		result.update({'exported': False})
		data['module-Directory Search'] = result
		fname = f'{output["directory"]}/directory_enum.{output["format"]}'
		output['file'] = fname
		export(output, data)


def hammer(target, threads, tout, wdlist, redir, sslv, dserv, output, data, filext):
	print(f'\n[!] Starting Directory Enum...\n')
	print(f'[+] Threads          : {threads}')
	print(f'[+] Timeout          : {tout}')
	print(f'[+] Wordlist         : {wdlist}')
	print(f'[+] Allow Redirects  : {redir}')
	print(f'[+] SSL Verification : {sslv}')
	print(f'[+] DNS Servers      : {dserv}')
	with open(wdlist, 'r') as wordlist:
		num_words = sum(1 for i in wordlist)
	print(f'[+] Wordlist Size    : {num_words}')
	print(f'[+] File Extensions  : {filext}\n')
	if len(filext) != 0:
		total_num_words = num_words * (len(filext.split(',')) + 1)
	else:
		total_num_words = num_words

	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	loop.run_until_complete(run(target, threads, tout, wdlist, redir, sslv, dserv, filext, total_num_words))
	dir_output(output, data)
	loop.close()
