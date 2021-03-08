#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (C) 2017 Heinlein Support GmbH
# Robert Sander <r.sander@heinlein-support.de>
#

import argparse
import checkmkapi
import pprint

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--url',
                    required=False,
                    help='URL to Check_MK site')
parser.add_argument('-u', '--username',
                    required=False,
                    help='name of the Automation user')
parser.add_argument('-p', '--password',
                    required=False)
parser.add_argument('-a', '--append',
                    required=False,
                    help='append this to the hypervisor name if not already there (usually the domainname)')
args = parser.parse_args()

mapi = checkmkapi.MultisiteAPI(args.url, args.username, args.password)
wato = checkmkapi.CMKRESTAPI(args.url, args.username, args.password)

resp = mapi.view(view_name='servicedesc', service='ESX Hostsystem')
hosts = {}
for item in resp:
    node = False
    if item['svc_plugin_output'].startswith('Running on '):
        node = item['svc_plugin_output'][11:]
        if not node.endswith(args.append):
            node += args.append
    hosts[item['host']] = node

watohosts, etags = wato.get_all_hosts()

changes = False
for host in hosts.keys():
    if host in watohosts:
        watohost = watohosts[host]
    else:
        continue
    if watohost['attributes'].get('parents', []) != [ hosts[host] ]:
        if hosts[host]:
            print("%s gets %s as parent" % (host, hosts[host]))
            wato.edit_host(host, etag=etags[host], set_attr={'parents': [ hosts[host] ]})
            changes = True
        elif len(watohost['attributes'].get('parents', [])) == 1:
            print("%s gets no specific parent" % (host, hosts[host]))
            wato.edit_host(host, etag=etags[host], unset_attr=['parents'])
            changes = True
if changes:
    wato.activate()
