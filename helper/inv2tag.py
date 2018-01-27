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

resp = mapi.view(view_name='opsys')
result = {}
for info in resp:
    for key, value in info.iteritems():
        if key not in result:
            result[key] = set()
        result[key].add(value)

pprint.pprint(result)
