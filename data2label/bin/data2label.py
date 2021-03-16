#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (C) 2017 Heinlein Support GmbH
# Robert Sander <r.sander@heinlein-support.de>
#

import argparse
import checkmkapi
import re
import copy
from pprint import pprint

def get_host_labels(hostname):
    host, etag = wato.get_host(hostname)

    orig_labels = host['extensions']['attributes'].get('labels', {})
    host_labels = {}

    # only use labels that do not start with label_prefix
    for attr in conf_labelmap.keys():
        for label, value in orig_labels.items():
            if not label.startswith(conf['label_prefix'][attr]):
                host_labels[label] = value

    return host_labels, orig_labels, etag

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--url', help='URL to Check_MK site')
parser.add_argument('-u', '--username', help='name of the automation user')
parser.add_argument('-p', '--password', help='secret of the automation user')
parser.add_argument('-c', '--config', required=True, help='Path to config file')
parser.add_argument('-d', '--dump', action="store_true", help='Dump unique values from the view')
args = parser.parse_args()

conf = eval(open(args.config, 'r').read())
conf_labelmap = {}
for attr, patterns in conf['labelmap'].items():
    conf_labelmap[attr] = {}
    for pattern, labels in patterns.items():
        conf_labelmap[attr][re.compile(pattern, re.IGNORECASE)] = labels

mapi = checkmkapi.MultisiteAPI(args.url, args.username, args.password)
wato = checkmkapi.CMKRESTAPI(args.url, args.username, args.password)

resp = mapi.view(conf['view_name'], **conf.get('args', {}))

if args.dump:
    #
    # get uniq values from view
    #
    result = {}
    for info in resp:
        for key, value in info.items():
            if key not in result:
                result[key] = set()
            result[key].add(value)
    pprint(result)
else:
    changes = False
    
    host_info = {}
    
    for info in resp:
        hostname = info['host']
        host_info.setdefault(hostname, [])
        host_info[hostname].append(info)

    for hostname, infos in host_info.items():
        try:
            host_labels, orig_labels, etag = get_host_labels(hostname)
        except Exception:
            raise
        for info in infos:
            for attr, patterns in conf_labelmap.items():
                if attr in info:
                    for pattern, setlabels in patterns.items():
                        if pattern.search(info[attr]):
                            # set labels if pattern matches
                            for label in setlabels:
                                host_labels[u'%s%s' % (conf['label_prefix'][attr], label)] = conf['label_value'][attr]

        if host_labels != orig_labels:
            print("Setting labels for %s to %s (etag=%s)" % (hostname, host_labels, etag))
            wato.edit_host(hostname, etag=etag, set_attr={'labels': host_labels})
            changes = True
    if changes:
        wato.activate()
        wato.bake_agents()
