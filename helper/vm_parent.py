#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (C) 2017 Heinlein Support GmbH
# Robert Sander <r.sander@heinlein-support.de>
#

import argparse
import requests
import pprint

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--url', required=True, help='URL to Check_MK site')
parser.add_argument('-u', '--username', required=True, help='name of the Automation user')
parser.add_argument('-p', '--password', required=True)
# parser.add_argument('-d', '--desc', required=False, help='Service Description to use', '
args = parser.parse_args()

if args.url[-1] == '/':
    if not args.url.endswith('check_mk/'):
        args.url += 'check_mk/'
else:
    if not args.url.endswith('check_mk'):
        args.url += '/check_mk/'    

params = {
    'output_format': 'json',
    'service': 'ESX Hostsystem',
    'view_name': 'servicedesc',
    '_username': args.username,
    '_secret': args.password,
}
              
resp = requests.get(args.url + 'view.py', params=params)
for state, icons, hostname, output, perfometer in resp.json():
    print hostname, output
