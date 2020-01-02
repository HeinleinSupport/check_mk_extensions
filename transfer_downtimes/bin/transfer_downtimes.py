#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# This tool reads the history logfile from the source instance
# and greps for DOWNTIME commands which are then passed to the
# command pipe in another instance.

# (c) 2019 Heinlein Support GmbH
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

import os
import sys
import logwatcher
import argparse
import daemon
import daemon.pidfile

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--source', help='Source site', required=True)
parser.add_argument('-t', '--dest', help='Destination site', default=os.environ['OMD_SITE'])
parser.add_argument('-p', '--pidfile', help='PID file', default=os.path.join(os.environ['OMD_ROOT'], 'tmp/run/transfer_downtimes.pid'))
parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output', default=False)
args = parser.parse_args()

if args.source == args.dest:
    print "Do not do this! It will create an infinite loop."
    sys.exit(1)

logfilename = os.path.join('/omd/sites', args.source, 'var/check_mk/core/history')
cmdfilename = os.path.join('/omd/sites', args.dest, 'tmp/run/nagios.cmd')

def handle_lines(filename, lines):
    for line in lines:
        if args.debug:
            print line
        if 'SCHEDULE_HOST_DOWNTIME' in line or 'SCHEDULE_SVC_DOWNTIME' in line:
            words = line.split(' ')
            del(words[1:3])
            cmd = ' '.join(words)
            if args.debug:
                print "found DOWNTIME command: %s" % cmd
                print "writing to %s" % cmdfilename
            cmdfile = open(cmdfilename, 'w')
            cmdfile.write(cmd)
            cmdfile.close()

def tailer():
    watcher = logwatcher.LogWatcher(os.path.dirname(logfilename), handle_lines, files=[os.path.basename(logfilename)])
    watcher.loop(interval=2)

if __name__ == '__main__':
    if args.debug:
        tailer()
    else:
        with daemon.DaemonContext(pidfile=daemon.pidfile.PIDLockFile(args.pidfile),
                                  working_directory=os.environ['OMD_ROOT'],
                                  stderr=sys.stderr):
            tailer()
