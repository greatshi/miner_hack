#!/usr/bin/env python
#coding=utf-8

import shodan

def shodanSearch(keywords, SHODAN_API_KEY):
    SHODAN_API_KEY = SHODAN_API_KEY
    api = shodan.Shodan(SHODAN_API_KEY)

    iplist = []
    total = 0

    try:
        results = api.search(keywords)
        total = int(results['total'])
        for result in results['matches']:
            iplist.append({"ip":result['ip_str'],"country":result['location']['country_name']})
        return total, iplist
    except shodan.APIError, e:
        print 'Error: %s' % e

def save_ip():
    with open('shodan_api_key.pem', 'r') as f:
        SHODAN_API_KEY = f.read().split('\n')[0]
    total, iplist = shodanSearch('(antminer)', SHODAN_API_KEY)
    f = open('ip.txt', 'w+')
    for ip in iplist:
        f.write(ip['ip'] + '\n')
    f.close()
    print 'ok'

def main():
    save_ip()

if __name__ == '__main__':
    main()
