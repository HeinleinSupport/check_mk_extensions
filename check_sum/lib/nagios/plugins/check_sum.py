#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2016 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>
#

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  This file is distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# tails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

import argparse
import os
import socket
import json
import pprint

#
# MKLivestatus helper from https://github.com/arthru/python-mk-livestatus
# Copyright (c) 2011, Michael Fladischer
#

class Query(object):
    def __init__(self, conn, resource):
        self._conn = conn
        self._resource = resource
        self._columns = []
        self._filters = []
        self._stats = []

    def call(self):
        try:
            data = bytes(str(self), 'utf-8')
        except TypeError:
            data = str(self)
        return self._conn.call(data)

    __call__ = call

    def __str__(self):
        request = 'GET %s' % (self._resource)
        if self._columns and any(self._columns):
            request += '\nColumns: %s' % (' '.join(self._columns))
        if self._filters:
            for filter_line in self._filters:
                if filter_line.startswith('Or: ') or filter_line.startswith('And: '):
                    request += '\n%s' % (filter_line)
                else:
                    request += '\nFilter: %s' % (filter_line)
        if self._stats:
            for stats_line in self._stats:
                request += '\nStats: %s' % (stats_line)
        request += '\nOutputFormat: json\nColumnHeaders: on\n'
        return request

    def columns(self, *args):
        self._columns = args
        return self

    def filter(self, filter_str):
        self._filters.append(filter_str)
        return self

    def stats(self, stats_str):
        self._stats.append(stats_str)
        return self

class Socket(object):
    def __init__(self, peer):
        self.peer = peer

    def __getattr__(self, name):
        return Query(self, name)

    def call(self, request):
        try:
            if len(self.peer) == 2:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            else:
                s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            s.connect(self.peer)
            s.send(request)
            s.shutdown(socket.SHUT_WR)
            rawdata = s.makefile().read()
            if not rawdata:
                return []
            data = json.loads(rawdata)
            return [dict(zip(data[0], value)) for value in data[1:]]
        finally:
            s.close()

#
# End MKLivestatus Helper
#

home = os.environ.get('OMD_ROOT')
if home:
    omd = True
    livesocketname = 'unix:' + home + '/tmp/run/live'
else:
    omd = False
    home = os.environ.get('HOME')
    livesocketname = 'unix:/usr/local/nagios/var/rw/live'

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--live', help='Livestatus API socket (default: %s)' % livesocketname, default=livesocketname)
parser.add_argument('-n', '--hosts', required=True, nargs='+')
parser.add_argument('-s', '--service', help='Service Description', required=True)
parser.add_argument('-d', '--datasource', help='Datasource Name', nargs='+')
parser.add_argument('-w', '--warn', help='Warning thresholds for the datasources, must be the same length as datasources', nargs='+')
parser.add_argument('-c', '--crit', help='Critical thresholds for the datasources, must be the same length as datasources', nargs='+')
args=parser.parse_args()

if args.datasource:
    if args.warn:
        if len(args.datasource) != len(args.warn):
            parser.print_help()
            parser.exit(1)
    if args.crit:
        if len(args.datasource) != len(args.crit):
            parser.print_help()
            parser.exit(1)

if args.live.startswith('unix:'):
    live = Socket(args.live[5:])
elif args.live.startswith('tcp://'):
    host, port = args.live[6:].split(':')
    live = Socket((host, int(port)))

query = live.services

for hostname in args.hosts:
    query = query.filter('host_name = %s' % hostname)
query = query.filter('Or: %d' % len(args.hosts))
query = query.filter('description = %s' % args.service).stats('sum perf_data')

results = query.call()

msg = ['Values are from %s service %s' % (', '.join(args.hosts), args.service) ]
pdata = []
rc = 0

sign = { 0: '', 1: '(!)', 2: '(!!)' }

for result in results:
    for perfdata in result['stats_1'].split():
        dsname, value = perfdata.split('=')
        if args.datasource and dsname in args.datasource:
            value = float(value)
            res = 0
            index = args.datasource.index(dsname)
            pd = [ "%s=%s" % ( dsname, value ) ]
            if args.warn:
                warn = args.warn[index]
                pd.append(warn)
                if warn:
                    warn = float(warn)
                    if value > warn:
                        res = 1
            if args.crit:
                crit = args.crit[index]
                pd.append(crit)
                if crit:
                    crit = float(crit)
                    if value > crit:
                        res = 2
            pdata.append(";".join(pd))
            if res > rc:
                rc = res
            msg.append("%s is %0.2f%s" % (dsname, value, sign[res]))
        if not args.datasource:
            pdata.append(perfdata)
            msg.append("%s is %s" % (dsname, value))
    
print "%s|%s" % (msg[0], " ".join(pdata))
print "\n".join(msg[1:])
parser.exit(rc)
