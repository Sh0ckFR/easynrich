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

	def launch_subfinder(self):
		'''Start subfinder on the domain'''
		if sys.argv[1].endswith('.txt'):
			with open(sys.argv[1], 'r') as file:
				for line in file:
					line = line.strip()
					if len(line) > 0:
						subprocess.Popen(['subfinder', '-d', line, '-o', f'subfinder-{line}.txt']).wait()
		else:
			subprocess.Popen(['subfinder', '-d', sys.argv[1], '-o', f'subfinder-{sys.argv[1]}.txt']).wait()

	def get_ip_addresses(self):
		'''Get the IP addresses from the subdomains'''
		if sys.argv[1].endswith('.txt'):
			with open(sys.argv[1], 'r') as file:
				for line in file:
					line = line.strip()
					if len(line) > 0:
						with open(f'subfinder-{line}.txt', 'r') as subfile:
							for line in subfile:
								line = line.strip()
								if len(line) > 0:
									try:
										ip_address = socket.gethostbyname(line)
										if ip_address not in self.ip_list:
											self.ip_list.append(ip_address)
									except (socket.gaierror, UnicodeError):
										pass
		else:
			with open(f'subfinder-{sys.argv[1]}.txt', 'r') as file:
				for line in file:
					line = line.strip()
					if len(line) > 0:
						try:
							ip_address = socket.gethostbyname(line)
							if ip_address not in self.ip_list:
								self.ip_list.append(ip_address)
						except (socket.gaierror, UnicodeError):
							pass

	def launch_nrich(self):
		'''Start nrich on the IP addresses from the subdomains'''
		with open('ip_addresses.txt', 'w') as file:	
			for ip_address in self.ip_list:
				file.write(f'{ip_address}\r\n')
		subprocess.Popen(['nrich', 'ip_addresses.txt']).wait()

def main():
	'''Main'''
	dns2nrich = Dns2nrich()
	dns2nrich.launch_subfinder()
	dns2nrich.get_ip_addresses()
	dns2nrich.launch_nrich()

if __name__ == '__main__':
	main()
