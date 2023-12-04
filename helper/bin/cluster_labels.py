#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (C) 2023 Heinlein Support GmbH
# Robert Sander <r.sander@heinlein-support.de>
#

import argparse
import checkmkapi
from pprint import pprint

label_prefix = "cluster/"

def get_host_labels(hostname):
    host, etag = wato.get_host(hostname)

    orig_labels = host['extensions']['attributes'].get('labels', {})
    host_labels = {}

    for label, value in orig_labels.items():
        if not label.startswith(label_prefix):
            host_labels[label] = value

    return host_labels, orig_labels, etag

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--url',
                    required=False,
                    help='URL to Check_MK site')
parser.add_argument('-u', '--username',
                    required=False,
                    help='name of the Automation user')
parser.add_argument('-p', '--password',
                    required=False)
parser.add_argument('-i', '--site',
                    required=False)
args = parser.parse_args()

mapi = checkmkapi.MultisiteAPI(args.url, args.username, args.password)
wato = checkmkapi.CMKRESTAPI(args.url, args.username, args.password)

if args.site:
    resp = mapi.view(view_name='cluster_hosts', filled_in='filter', site=args.site)
else:
    resp = mapi.view(view_name='cluster_hosts')
hosts = {}
for item in resp:
    # pprint(item)
    hostname = item.get('host')
    if hostname:
        hosts.setdefault(hostname, {})
        hosts[hostname]['cluster'] = item.get('inv_software_applications_check_mk_cluster_is_cluster')
        if hosts[hostname]['cluster']:
            for node in item.get('inv_software_applications_check_mk_cluster_nodes', {}).get('Table', {}).get('Rows', []):
                hosts.setdefault(node['name'], {'node_of': []})
                hosts[node['name']]['node_of'].append(hostname)

# pprint(hosts)

changes = False
for hostname in hosts.keys():
    # pprint(hostname)
    
    try:
        host_labels, orig_labels, etag = get_host_labels(hostname)
    except Exception:
        raise

    # pprint(host_labels)
    # pprint(orig_labels)
    # pprint(etag)

    if hosts[hostname]['cluster']:
        host_labels['cluster/host'] = 'yes'
    for cluster in hosts[hostname].get('node_of', []):
        host_labels['cluster/node_of/%s' % cluster] = 'yes'

    if host_labels != orig_labels:
        print("Setting labels for %s to %s (etag=%s)" % (hostname, host_labels, etag))
        wato.edit_host(hostname, etag=etag, update_attr={'labels': host_labels})
        changes = True
    
if changes:
    wato.activate()
