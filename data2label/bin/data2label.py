#!/usr/bin/env python
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

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--url', required=True, help='URL to Check_MK site')
parser.add_argument('-u', '--username', required=True, help='name of the automation user')
parser.add_argument('-p', '--password', required=True, help='secret of the automation user')
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
wato = checkmkapi.WATOAPI(args.url, args.username, args.password)

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

    host_labels = {}
    orig_labels = {}
    
    def get_host_labels(hostname):
        if hostname not in host_labels:
            print "Getting labels…"
            host = wato.get_host(hostname)

            host_labels[hostname] = host['attributes'].get('labels', {})
            orig_labels[hostname] = copy.deepcopy(host_labels[hostname])

            # remove labels that start with label_prefix
            for attr in conf_labelmap.keys():
                for label in host_labels[hostname].keys():
                    if label.startswith(conf['label_prefix'][attr]):
                        del(host_labels[hostname][label])
            print "host_labels[%s] = %s" % (hostname, host_labels[hostname])
            print "orig_labels[%s] = %s" % (hostname, orig_labels[hostname])

    for info in resp:
        hostname = info['host']
        print hostname
        try:
            get_host_labels(hostname)
        except RuntimeError:
            continue
        for attr, patterns in conf_labelmap.items():
            if attr in info:
                print attr, info[attr]
                for pattern, setlabels in patterns.items():
                    if pattern.search(info[attr]):
                        # set labels if pattern matches
                        for label in setlabels:
                            host_labels[hostname][u'%s%s' % (conf['label_prefix'][attr], label)] = conf['label_value'][attr]
                            print host_labels[hostname]

    for hostname, labels in host_labels.items():
        if labels != orig_labels[hostname]:
            print "Setting labels for %s to %s" % (hostname, labels)        
            wato.edit_host(hostname, set_attr={'labels': labels})
            changes = True
    if changes:
        wato.activate()
        wato.bake_agents()
