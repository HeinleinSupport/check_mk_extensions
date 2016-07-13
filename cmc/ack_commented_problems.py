#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2016 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  This file is distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

"""Creates commands to acknowledge previously acknowledged host and
service problems after migrating from Nagios core to CMC."""

import requests
import datetime
import argparse
import getpass

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', required=True, help='Automation User')
parser.add_argument('-p', '--password', required=False, help='Automation Secret')
parser.add_argument('-H', '--host', required=True, help='Hostname')
parser.add_argument('-s', '--site', required=True, help='Monitoring Site')
args = parser.parse_args()

if not args.password:
    args.password = getpass.getpass('Please enter password for %s: ' % args.username)

baseurl = 'https://%s/%s/check_mk/view.py' % (args.host, args.site)
services_to_ack = {}

#
# Get unacknowledged hosts with a comment
#
r = requests.get(baseurl, params={'_username': args.username,
                                  '_secret': args.password,
                                  'output_format': 'json',
                                  'view_name': 'hostproblems',
                                  'is_host_acknowledged': '0'})
hosts = r.json()
columns = {}
for i in range(len(hosts[0])):
    columns[hosts[0][i]] = i
for host in hosts[1:]:
    if 'comment' in host[columns['host_icons']]:
        if host[columns['host']] not in services_to_ack:
            services_to_ack[host[columns['host']]] = []
        services_to_ack[host[columns['host']]].append('')

#
# Get unacknowledged services with a comment
#
r = requests.get(baseurl, params={'_username': args.username,
                                  '_secret': args.password,
                                  'output_format': 'json',
                                  'view_name': 'svcproblems',
                                  'is_service_acknowledged': '0'})
services = r.json()
columns = {}
for i in range(len(services[0])):
    columns[services[0][i]] = i
for service in services[1:]:
    if 'comment' in service[columns['service_icons']]:
        if service[columns['host']] not in services_to_ack:
            services_to_ack[service[columns['host']]] = []
        services_to_ack[service[columns['host']]].append(service[columns['service_description']])

#
# Get all comments and match with service list from above
#
r = requests.get(baseurl, params={'_username': args.username,
                                  '_secret': args.password,
                                  'output_format': 'json',
                                  'po_ts_date': '0',
                                  'po_ts_format': '1',
                                  'view_name': 'comments'})                                  
comments = r.json()
columns = {}
for i in range(len(comments[0])):
    columns[comments[0][i]] = i
for comment in comments[1:]:
    if comment[columns['host']] in services_to_ack and comment[columns['service_description']] in services_to_ack[comment[columns['host']]]:
        # Print commands to feed to command pipe
        if comment[columns['service_description']] == '':
            print '[%s] DEL_HOST_COMMENT;%s' % (datetime.datetime.now().strftime('%s'),
                                                comment[columns['comment_id']])
            print '[%s] ACKNOWLEDGE_HOST_PROBLEM;%s;1;0;0;%s;%s' % (datetime.datetime.strptime(comment[columns['comment_time']], '%Y-%m-%d %H:%M:%S').strftime('%s'),
                                                                    comment[columns['host']],
                                                                    comment[columns['comment_author']],
                                                                    comment[columns['comment_comment']])
        else:
            print '[%s] DEL_SVC_COMMENT;%s' % (datetime.datetime.now().strftime('%s'),
                                               comment[columns['comment_id']])
            print '[%s] ACKNOWLEDGE_SVC_PROBLEM;%s;%s;1;0;0;%s;%s' % (datetime.datetime.strptime(comment[columns['comment_time']], '%Y-%m-%d %H:%M:%S').strftime('%s'),
                                                                      comment[columns['host']],
                                                                      comment[columns['service_description']],
                                                                      comment[columns['comment_author']],
                                                                      comment[columns['comment_comment']])
