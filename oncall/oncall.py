#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (C) 2016 Heinlein Support GmbH
# Robert Sander <r.sander@heinlein-support.de>

# in ~/etc
oncall_filename = 'oncall.csv'
# Format is:
# start;end;notify_plugin;adminonduty
# notify_plugin and adminonduty columns may be lists
# lists are separated by comma
# notify_plugin may be 'off duty' (see below default_offduty)
# to set an entry explicitely to off duty
# adminonduty can contain user or group names

import os
import csv
import time
from pprint import pprint
import sys

omdroot = os.environ.get('OMD_ROOT')
now = time.gmtime() # dates and times are in UTC
timeformat = '%Y-%m-%dT%H:%M:%S'
oncall_group = u'oncall'
default_desc = u'oncall'
default_rule = {'comment': u'When this rule is disabled, the user is on-call.',
                'description': default_desc,
                'docu_url': '',
                'disabled': False,
                }
default_offduty = 'off duty'
onduty = {}
offduty = []
notify_plugins = set()

def duty(rule):
    if rule['disabled']:
        return "on duty"
    else:
        return "off duty"


vars = { 'notification_rules' : [] }
execfile(os.path.join(omdroot, 'etc/check_mk/conf.d/wato/notifications.mk'), vars, vars)
for rule in vars['notification_rules']:
    if rule['allow_disable'] and 'contact_match_groups' in rule and oncall_group in rule['contact_match_groups']:
        notify_plugins.add(rule['notify_plugin'][0])

vars = { 'contacts': {} }
execfile(os.path.join(omdroot, 'etc/check_mk/conf.d/wato/contacts.mk'), vars, vars)
contacts = vars['contacts']
         
with open(os.path.join(omdroot, 'etc', oncall_filename), 'rb') as oncallfile:
    csvreader = csv.DictReader(oncallfile, delimiter=';')
    for row in csvreader:
        start = time.strptime(row['start'], timeformat)
        end = time.strptime(row['end'], timeformat)
        if start <= now and now <= end:
            for part in row['adminonduty'].split(','):
                if row['notify_plugin'] == default_offduty:
                    offduty.append(part)
                else:
                    if part not in onduty:
                        onduty[part] = set()
                    onduty[part].update(row['notify_plugin'].split(','))

#pprint(onduty)
#pprint(offduty)

for user, data in contacts.iteritems():
    print user
    user_attr_oncall = ( 'contactgroups' in data and oncall_group in data['contactgroups'] )
    other_rules = []
    if 'notification_rules' in data:
        for rule in data['notification_rules']:
            if rule['description'] != default_desc:
                other_rules.append(rule)
    contacts[user]['notification_rules'] = other_rules
    notify_plugins_onduty = []
    groupduty = False
    for contactgroup in data['contactgroups']:
        if ( contactgroup in onduty ) and ( contactgroup not in offduty ):
            groupduty = contactgroup
    if user_attr_oncall:
        if ( user in onduty or groupduty ) and ( user not in offduty ):
            if user in onduty:
                notify_plugins_onduty = onduty[user]
            else:
                notify_plugins_onduty = onduty[groupduty]
            for notify_plugin in notify_plugins_onduty:
                rule = default_rule.copy()
                rule['contact_users'] = [ user ]
                rule['notify_plugin'] = (notify_plugin, None)
                rule['disabled'] = True
                contacts[user]['notification_rules'].append(rule)
        for notify_plugin in notify_plugins:
            if notify_plugin not in notify_plugins_onduty:
                rule = default_rule.copy()
                rule['contact_users'] = [ user ]
                rule['notify_plugin'] = (notify_plugin, None)
                contacts[user]['notification_rules'].append(rule)

print """# Written by oncall.py
# encoding: utf-8

contacts.update("""
pprint(contacts)
print ")"
