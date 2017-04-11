#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2017 Heinlein Support GmbH
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

import sys
import threading
import time
import subprocess
import argparse

logfilename = '/var/log/apache2/access.log'
outputfilename = '/tmp/apachecount'

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--logfile', help='path to Apache logfile', default=logfilename)
parser.add_argument('-o', '--output', help='Output file name (check_MK agent spool file)', default=outputfilename)
parser.add_argument('-s', '--sleep', type=int, help='Seconds to sleep between writes to output file', default=30)
parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output', default=False)
args = parser.parse_args()

tail = ['/usr/bin/tail', '-qF', args.logfile]
awk = ['/usr/bin/awk', '/POST .user.authentication.posti HTTP/ { print $9 ; fflush(); }']
status_count = {'http_200': 0,
                'http_401': 0}

def writer():
    while True:
        if not r.is_alive():
            break
        time.sleep(args.sleep)
        if args.debug:
            print "Writing status_count = %s to %s" % (status_count, args.output)
        with open(args.output, 'w') as outputfile:
            outputfile.write('<<<apachecount>>>\n')
            for status, count in status_count.iteritems():
                outputfile.write('%s %d\n' % (status, status_count[status]))

def reader():
    if args.debug:
        print "Starting %s" % tail
    tailp = subprocess.Popen(tail, bufsize=1, stdout = subprocess.PIPE, close_fds=True)
    if args.debug:
        print "Starting %s" % awk
    awkp = subprocess.Popen(awk, bufsize=1, stdin = tailp.stdout, stdout = subprocess.PIPE, close_fds=True)
    while True:
        if args.debug:
            print "Reading line"
        line = awkp.stdout.readline()
        if tailp.poll() or awkp.poll() or not line:
            if args.debug:
                print "Pipe is broken"
            break
        if args.debug:
            print line
        status = 'http_%s' % line.strip()
        if status not in status_count:
            status_count[status] = 0
        if status_count[status] == sys.maxsize:
            status_count[status] = 1
        else:
            status_count[status] += 1
        if args.debug:
            print "%s is now %d" % (status, status_count[status])

if args.debug:
    print "Starting reader thread"
r = threading.Thread(target=reader)
r.start()
if args.debug:
    print "Started read thread"

if args.debug:
    print "Starting writer thread"
w = threading.Thread(target=writer)
w.daemon = True
w.start()
if args.debug:
    print "Started writer thread"

r.join()
