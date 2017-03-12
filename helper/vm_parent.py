#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (C) 2017 Heinlein Support GmbH
# Robert Sander <r.sander@heinlein-support.de>
#

import argparse
import checkmkapi
import pprint

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

# pprint.pprint(hosts)

changes = False
for host in hosts.keys():
    watohost = wato.get_host(host)
    if watohost['attributes']['parents'] != [ hosts[host] ]:
        print "%s gets %s as parent" % (host, hosts[host])
        changes = True
        # wato.edit_host(host, set_attr={'parents': [ hosts[host] ]})
if changes:
    # wato.activate()
    pass
