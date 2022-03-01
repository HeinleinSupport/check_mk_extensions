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
parser.add_argument('-r', '--remove',
                    action='store_true',
                    required=False,
                    help="remove the domainname from the hypervisor's name")
parser.add_argument('-i', '--site',
                    required=False)
args = parser.parse_args()

mapi = checkmkapi.MultisiteAPI(args.url, args.username, args.password)
wato = checkmkapi.CMKRESTAPI(args.url, args.username, args.password)

if args.site:
    resp = mapi.view(view_name='servicedesc', service='ESX Hostsystem', filled_in='filter', site=args.site)
else:
    resp = mapi.view(view_name='servicedesc', service='ESX Hostsystem')
hosts = {}
for item in resp:
    node = False
    if item['svc_plugin_output'].startswith('Running on '):
        node = item['svc_plugin_output'][11:]
        if args.remove:
            node = node.split('.')[0]
        if args.append and not node.endswith(args.append):
            node += args.append
    hosts[item['host']] = node

changes = False
for host in hosts.keys():
    try:
        watohost, etag = wato.get_host(host, effective_attr=True)
    except:
        continue
    if watohost['extensions']['effective_attributes'].get('parents', []) != [ hosts[host] ]:
        if hosts[host]:
            print("%s gets %s as parent" % (host, hosts[host]))
            wato.edit_host(host, etag=etag, update_attr={'parents': [ hosts[host] ]})
            changes = True
        elif len(watohost['extensions']['attributes'].get('parents', [])) == 1:
            print("%s gets no specific parent" % (host, hosts[host]))
            wato.edit_host(host, etag=etag, unset_attr=['parents'])
            changes = True
if changes:
    wato.activate()
