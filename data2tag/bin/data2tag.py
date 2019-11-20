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
import pprint

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--url', required=True, help='URL to Check_MK site')
parser.add_argument('-u', '--username', required=True, help='name of the automation user')
parser.add_argument('-p', '--password', required=True, help='secret of the automation user')
parser.add_argument('-c', '--config', required=True, help='Path to config file')
parser.add_argument('-d', '--dump', action="store_true", help='Dump unique values from the view')
args = parser.parse_args()

conf = eval(open(args.config, 'r').read())
conf_tagmap = {}
for attr, patterns in conf['tagmap'].iteritems():
    conf_tagmap[attr] = {}
    for pattern, settags in patterns.iteritems():
        conf_tagmap[attr][re.compile(pattern, re.IGNORECASE)] = settags

mapi = checkmkapi.MultisiteAPI(args.url, args.username, args.password)
wato = checkmkapi.WATOAPI(args.url, args.username, args.password)

resp = mapi.view(conf['view_name'], **conf.get('args', {}))

#
# get uniq values from view
#
if args.dump:
    result = {}
    for info in resp:
        for key, value in info.iteritems():
            if key not in result:
                result[key] = set()
            result[key].add(value)
    pprint.pprint(result)
else:
    changes = False
    hosts = wato.get_all_hosts()
    for info in resp:
        if info['host'] not in hosts:
            continue
        print info['host']
        tags = {}
        for attr, patterns in conf_tagmap.iteritems():
            if attr in info:
                pprint.pprint(info[attr])
                for pattern, settags in patterns.iteritems():
                    if pattern.search(info[attr]):
                        for taggroup, tag in settags.iteritems():
                            if taggroup in hosts[info['host']]['attributes']:
                                if hosts[info['host']]['attributes'][taggroup] != tag:
                                    tags[taggroup] = tag
                            else:
                                tags[taggroup] = tag
        print tags

        if tags:
            wato.edit_host(info['host'], set_attr=tags)
            changes = True
    if changes:
        wato.activate()
