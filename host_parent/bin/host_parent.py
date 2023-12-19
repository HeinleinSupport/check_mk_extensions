#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (C) 2023 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>
#

# Needs a view "hostparents":


import argparse
import checkmkapi
from pprint import pprint

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
    resp = mapi.view(view_name='hostparents', filled_in='filter', site=args.site)
else:
    resp = mapi.view(view_name='hostparents')
hosts = {}
for item in resp:
    node = False
    if item['svc_plugin_output.vmware'].startswith('Running on '):
        node = item['svc_plugin_output.vmware'][11:]
    elif item['svc_plugin_output.proxmox']:
        for key, value in map(lambda x: x.split(': ', 1),
                              item['svc_plugin_output.proxmox'].split(', ')):
            if key == 'Host':
                node = value
                break
    if node:
        if args.remove:
            node = node.split('.')[0]
        if args.append and not node.endswith(args.append):
            node += args.append
        if node != item['host_parents']:
            hosts[item['host']] = node

changes = False
for host, parent in hosts.items():
    try:
        watohost, etag = wato.get_host(host, effective_attr=True)
    except:
        continue
    if watohost['extensions']['effective_attributes'].get('parents', []) != [ parent ]:
        if parent:
            print("%s gets %s as parent" % (host, parent))
            wato.edit_host(host, etag=etag, update_attr={'parents': [ parent ]})
            changes = True
        elif len(watohost['extensions']['attributes'].get('parents', [])) == 1:
            print("%s gets no specific parent" % host)
            wato.edit_host(host, etag=etag, unset_attr=['parents'])
            changes = True
if changes:
    try:
        wato.activate()
    except checkmkapi.requests.exceptions.HTTPError as er:
        resp = er.response
        if resp.status_code != 401:
            raise
