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

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--url', help='URL to Check_MK site')
parser.add_argument('-u', '--username', help='name of the automation user')
parser.add_argument('-p', '--password', help='secret of the automation user')
parser.add_argument('-c', '--config', required=True, help='Path to config file')
parser.add_argument('-d', '--dump', action="store_true", help='Dump unique values from the view')
args = parser.parse_args()

conf = eval(open(args.config, 'r').read())
conf_tagmap = {}
for attr, patterns in conf['tagmap'].items():
    conf_tagmap[attr] = {}
    for pattern, settags in patterns.items():
        conf_tagmap[attr][re.compile(pattern, re.IGNORECASE)] = settags

mapi = checkmkapi.MultisiteAPI(args.url, args.username, args.password)
wato = checkmkapi.CMKRESTAPI(args.url, args.username, args.password)

resp = mapi.view(conf['view_name'], **conf.get('args', {}))

#
# get uniq values from view
#
if args.dump:
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
    hosts, etags = wato.get_all_hosts(attributes=False)

    # pprint(hosts)

    for info in resp:
        hostname = info['host']
        host_info.setdefault(hostname, {})
        for attr, value in info.items():
            host_info[hostname].setdefault(attr, [])
            host_info[hostname][attr].append(value)

    # pprint(host_info)

    for hostname, info in host_info.items():
        try:
            host, etag = wato.get_host(hostname)
        except Exception:
            raise
        # pprint(host)
        host_tags = host['extensions']['attributes']
        tags = {}
        unset_tags = []
        for attr, patterns in conf_tagmap.items():
            if attr in info:
                for pattern, settags in patterns.items():
                    for value in info[attr]:
                        if pattern.search(value):
                            for taggroup, tag in settags.items():
                                if host_tags.get(taggroup) != tag:
                                    tags[taggroup] = tag
        if tags or unset_tags:
            # pprint(tags)
            # pprint(unset_tags)
            wato.edit_host(hostname,
                           etag=etag,
                           update_attr=tags,
                           unset_attr=unset_tags)
            changes = True
        if hostname in hosts:
            del(hosts[hostname])

    # pprint(hosts)
    for hostname, url in hosts.items():
        try:
            host, etag = wato.get_host(hostname)
        except Exception:
            raise
        # pprint(host)
        host_tags = list(host['extensions']['attributes'].keys())
        unset_tags = []
        for attr, patterns in conf_tagmap.items():
            for pattern, settags in patterns.items():
                for taggroup, tag in settags.items():
                    if taggroup in host_tags:
                        unset_tags.append(taggroup)
        if unset_tags:
            # pprint(unset_tags)
            wato.edit_host(hostname, etag=etag, unset_attr=unset_tags)
            changes = True
            
    if changes:
        wato.activate()
