#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (C) 2017 Heinlein Support GmbH
# Robert Sander <r.sander@heinlein-support.de>
#

import argparse
import checkmkapi
import re
import pprint

tagmap = {
    'inv_software_os_name': {
        re.compile('centos', re.IGNORECASE): {'tag_opsys': 'redhat'},
        re.compile('debian', re.IGNORECASE): {'tag_opsys': 'debian'},
        re.compile('suse', re.IGNORECASE):   {'tag_opsys': 'suse'},
        re.compile('ubuntu', re.IGNORECASE): {'tag_opsys': 'ubuntu'},
#        re.compile('vmware', re.IGNORECASE): {'tag_opsys': 'esxi'},
        re.compile('xenserver', re.IGNORECASE): {'tag_opsys': 'redhat'},
        re.compile('Microsoft Windows 7'): {'tag_opsys': 'win7'},
        re.compile('Microsoft Windows Server 2008'): {'tag_opsys': 'win2008'},
        re.compile('Microsoft Windows Server 2012'): {'tag_opsys': 'win2012'},
        re.compile('Microsoft Windows Server 2016'): {'tag_opsys': 'win2016'},
    },
}

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--url', required=True, help='URL to Check_MK site')
parser.add_argument('-u', '--username', required=True, help='name of the Automation user')
parser.add_argument('-p', '--password', required=True)
args = parser.parse_args()

mapi = checkmkapi.MultisiteAPI(args.url, args.username, args.password)
wato = checkmkapi.WATOAPI(args.url, args.username, args.password)

resp = mapi.view(view_name='opsys')

#
# get uniq values from view
#
#result = {}
#for info in resp:
#    for key, value in info.iteritems():
#        if key not in result:
#            result[key] = set()
#        result[key].add(value)
#pprint.pprint(result)

pprint.pprint(tagmap)

for info in resp:
    print info['host']
    tags = {}
    for attr, patterns in tagmap.iteritems():
        if attr in info:
            pprint.pprint(info[attr])
            for pattern, settags in patterns.iteritems():
                if pattern.search(info[attr]):
                    tags.update(settags)
    print tags

    # wato.edit_host(info['host'], set_attr=tags)

