#!/usr/bin/env python
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

oncall_group = u'oncall'
default_desc = u'oncall'
default_offduty = 'off duty'

import os
import csv
import time
from pprint import pprint, pformat
import argparse
import requests
import json
import warnings

omdroot = os.environ.get('OMD_ROOT')
omdsite = os.environ.get('OMD_SITE')
now = time.gmtime() # dates and times are in UTC
timeformat = '%Y-%m-%dT%H:%M'
default_rule = {'comment': u'When this rule is disabled, the user is on-call.',
                'description': default_desc,
                'docu_url': '',
                'disabled': False,
                }
onduty = {}
offduty = []
notify_plugins = set()

notification_rules_filename = os.path.join(omdroot, 'etc/check_mk/conf.d/wato/notifications.mk')
contacts_filename = os.path.join(omdroot, 'etc/check_mk/conf.d/wato/contacts.mk')

omdconfig = {}
execfile(os.path.join(omdroot, 'etc/omd/site.conf'), omdconfig, omdconfig)

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', required=True, help='name of the Check_MK automation user')
parser.add_argument('-s', '--secret', required=True)
args = parser.parse_args()

api_url = 'http://%s:%s/%s/check_mk/webapi.py' % (omdconfig['CONFIG_APACHE_TCP_ADDR'], omdconfig['CONFIG_APACHE_TCP_PORT'], omdsite)
api_creds = {'_username': args.username, '_secret': args.secret, 'output_format': 'json'}
api_activate = { 'action': 'activate_changes'}
api_activate.update(api_creds)

# print api_url
# print api_activate

#
# Read list of noticication plugins
# where recipients are limited to the oncall_group
#
vars = { 'notification_rules' : [] }
execfile(notification_rules_filename, vars, vars)
for rule in vars['notification_rules']:
    if rule['allow_disable'] and 'contact_match_groups' in rule and oncall_group in rule['contact_match_groups']:
        notify_plugins.add(rule['notify_plugin'][0])

# print "notify_plugins = %s" % pformat(notify_plugins)
        
#
# Read list of contacts
#
vars = { 'contacts': {} }
execfile(contacts_filename, vars, vars)
contacts = vars['contacts']

#
# Determine who is on call right now
#
with open(os.path.join(omdroot, 'etc', oncall_filename), 'rb') as oncallfile:
    csvreader = csv.DictReader(oncallfile, delimiter=';')
    for row in csvreader:
        try:
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
        except ValueError:
            print "unknown time format in %s" % row

print "onduty = %s" % pformat(onduty)
print "contacts = %s" % pformat(contacts)
            
#
# Set oncall rules
#
for user, data in contacts.iteritems():
    print "user = %s" % user
    user_attr_oncall = ( 'contactgroups' in data and oncall_group in data['contactgroups'] )
    other_rules = []
    if 'notification_rules' in data:
        for rule in data['notification_rules']:
            if rule['description'] != default_desc:
                other_rules.append(rule)
    contacts[user]['notification_rules'] = other_rules
    notify_plugins_onduty = []
    groupduty = False
    if 'contactgroups' in data:
        for contactgroup in data['contactgroups']:
            if ( contactgroup in onduty ) and ( contactgroup not in offduty ):
                groupduty = contactgroup
    
    print 'user_attr_oncall = %s' % pformat(user_attr_oncall)
    print 'offduty = %s' % pformat(offduty)
    print 'groupduty = %s' % pformat(groupduty)
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
                print "%s is on duty for %s" % (user, notify_plugin)
        for notify_plugin in notify_plugins:
            if notify_plugin not in notify_plugins_onduty:
                rule = default_rule.copy()
                rule['contact_users'] = [ user ]
                rule['notify_plugin'] = (notify_plugin, None)
                contacts[user]['notification_rules'].append(rule)
                print "%s is off duty for %s" % (user, notify_plugin)
    else:
        print "%s is not oncall" % user

#
# Write contacts
#
with open(contacts_filename, 'w') as contactsfile:
    contactsfile.write("# Written by oncall.py\n# encoding: utf-8\n\ncontacts.update(")
    contactsfile.write(pformat(contacts))
    contactsfile.write("\n)\n")

#
# Set Replication State
#
repstatus_filename = os.path.join(omdroot, "var/check_mk/wato/replication_status.mk")
sites = []
try:
    repstatus = eval(file(repstatus_filename).read())
except:
    repstatus = {}
for site in repstatus:
    repstatus[site]['need_sync'] = True
    sites.append(site)
open(repstatus_filename, 'w').write(pformat(repstatus))

#
# Activate Sites via WATO Web-API
#
def api_request(params, data=None, errmsg='Error', fail=True):
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        if data:
            resp = requests.post(api_url, verify=False, params=params, data='request=%s' % json.dumps(data))
        else:
            resp = requests.get(api_url, verify=False, params=params)
        try:
            resp1 = resp.json()
        except:
            raise
        resp = resp1
    if resp['result_code'] == 1:
        if fail:
            raise RuntimeError('%s: %s' % ( errmsg, resp['result'] ))
        else:
            print '%s: %s' % ( errmsg, resp['result'] )
    return resp['result']

for site in sites:
    print 'activating %s' % site
    api_request(params=api_activate, data={'sites': [site]})
