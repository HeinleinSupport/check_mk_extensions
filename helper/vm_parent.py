#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (C) 2017 Heinlein Support GmbH
# Robert Sander <r.sander@heinlein-support.de>
#

import argparse
import checkmkapi
import pprint

# for hypervisor hosts without FQDN
appenddomain = '.heinlein-hosting.de'
sites = ['heinlein']

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--url', required=True, help='URL to Check_MK site')
parser.add_argument('-u', '--username', required=True, help='name of the Automation user')
parser.add_argument('-p', '--password', required=True)
args = parser.parse_args()

mapi = checkmkapi.MultisiteAPI(args.url, args.username, args.password)
wato = checkmkapi.WATOAPI(args.url, args.username, args.password)

resp = mapi.view(view_name='servicedesc', service='ESX Hostsystem')
hosts = {}
for item in resp:
    if item['svc_plugin_output'].startswith('OK - Running on '):
        hosts[item['host']] = item['svc_plugin_output'][16:]
        if '.' not in hosts[item['host']]:
            hosts[item['host']] += appenddomain

watohosts = wato.get_all_hosts()

changes = False
for host in hosts.keys():
    if host in watohosts:
        watohost = watohosts[host]
    else:
        continue
    if watohost['attributes']['parents'] != [ hosts[host] ]:
        print "%s gets %s as parent" % (host, hosts[host])
        changes = True
        wato.edit_host(host, set_attr={'parents': [ hosts[host] ]})
if changes:
    wato.activate(sites)
