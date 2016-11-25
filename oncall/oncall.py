#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (C) 2016 Heinlein Support GmbH
# Robert Sander <r.sander@heinlein-support.de>

# in ~/etc
oncall_filename = 'oncall.csv'

import os
import csv
import time
from pprint import pprint
import sys

omdroot = os.environ.get('OMD_ROOT')
now = time.gmtime()
timeformat = '%Y-%m-%dT%H:%M:%S'
onduty = set()

with open(os.path.join(omdroot, 'etc', oncall_filename), 'rb') as oncallfile:
    csvreader = csv.DictReader(oncallfile, delimiter=';')
    for row in csvreader:
        start = time.strptime(row['start'], timeformat)
        end = time.strptime(row['end'], timeformat)
        if start <= now and now <= end:
            onduty.update(row['onduty'].split(','))
            
print onduty
        
contacts = {}
with open(os.path.join(omdroot, 'etc/check_mk/conf.d/wato/contacts.mk'), 'rb') as file:
    eval(file.read())

for user, data in contacts.iteritems():
    if 'notification_rules' in data:
        for rule in data['notification_rules']:
            if rule['description'] == 'oncall':
                if user in onduty:
                    rule['disabled'] = True
                else:
                    rule['disabled'] = False

print """# Written by Multisite UserDB
# encoding: utf-8

contacts.update("""
pprint(contacts)
print ")"
