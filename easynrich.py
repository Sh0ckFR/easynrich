#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Script to launch shodan-nrich on the subdomains of a specified domain
'''

import sys
import socket
import subprocess

class Dns2nrich:
	def __init__(self):
		self.ip_list = []

	def launch_subfinder(self, domain):
		'''Start subfinder on the domain'''
		print(f'[+] Start subfinder on the domain "{sys.argv[1]}" ...')
		subprocess.Popen(['subfinder', '-d', domain, '-o', 'subfinder.txt'])

	def get_ip_addresses(self):
		'''Get the IP addresses from the subdomains'''
		print(f'[+] Get the IP addresses from the subdomains, be patient...')
		with open('subfinder.txt', 'r') as file:
			for line in file:
				line = line.strip()
				if len(line) > 0:
					try:
						ip_address = socket.gethostbyname(line)
						if ip_address not in self.ip_list:
							self.ip_list.append(ip_address)
					except socket.gaierror:
						pass

	def launch_nrich(self):
		'''Start nrich on the ip addresses of the domains list'''
		print(f'[+] Start nrich on the IP addresses from the subdomains...')
		with open('ip_addresses.txt', 'w') as file:	
			for ip_address in self.ip_list:
				file.write(f'{ip_address}\r\n')
		subprocess.Popen(['nrich', 'ip_addresses.txt'])
		sys.exit(0)

def main():
	'''Main'''
	dns2nrich = Dns2nrich()
	dns2nrich.launch_subfinder(sys.argv[1])
	dns2nrich.get_ip_addresses()
	dns2nrich.launch_nrich()

if __name__ == '__main__':
	main()
