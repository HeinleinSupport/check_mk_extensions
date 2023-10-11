#!/usr/bin/env python2
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# +------------------------------------------------------------------+
# |             ____ _               _        __  __ _  __           |
# |            / ___| |__   ___  ___| | __   |  \/  | |/ /           |
# |           | |   | '_ \ / _ \/ __| |/ /   | |\/| | ' /            |
# |           | |___| | | |  __/ (__|   <    | |  | | . \            |
# |            \____|_| |_|\___|\___|_|\_\___|_|  |_|_|\_\           |
# |                                                                  |
# | Copyright Mathias Kettner 2016             mk@mathias-kettner.de |
# +------------------------------------------------------------------+
#
# This file is part of Check_MK.
# The official homepage is at http://mathias-kettner.de/check_mk.
#
# check_mk is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# tails. You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

# Check_MK-Agent-Plugin - memcached Status
#
# By default this plugin tries to detect all locally running memcached processes
# and to monitor them. If this is not good for your environment you might
# create an memcached.cfg file in MK_CONFDIR and populate the servers
# list to prevent executing the detection mechanism.

import os, sys, re, socket

# sample configuration:
# instances = [
#  ("localhost", 11211),
#  ("localhost", 11212)
# ]

config_file=os.path.join(os.environ.get("MK_CONFDIR", "/etc/check_mk"), "memcached.cfg")

# We have to deal with socket timeouts. Python > 2.6
# supports timeout parameter for the urllib2.urlopen method
# but we are on a python 2.5 system here which seem to use the
# default socket timeout. We are local here so  set it to 1 second.
socket.setdefaulttimeout(5.0)

# None or list of (ipaddress, port) tuples.
instances = None

if os.path.exists(config_file):
    execfile(config_file)

def parse_address_and_port(address_and_port):
    """
    parse address:port section from netstat or ss
    return address, port
    """
    server_address, _server_port = address_and_port.rsplit(":", 1)
    server_port = int(_server_port)

    # Use localhost when listening globally
    if server_address == "0.0.0.0":  # nosec - B104
        server_address = "127.0.0.1"
    elif server_address in ("::", "*", "[::]"):
        server_address = "[::1]"
    elif ":" in server_address and server_address[0] != "[":
        server_address = "[%s]" % server_address

    return server_address, server_port

def try_detect_servers():
    pids    = []
    results = []
    procs = [ 'memcached' ]

    #  ss lists parent and first level child processes
    #  last process in line is the parent:
    #    users:(("apache2",pid=123456,fd=3),...,("apache2",pid=123,fd=3))
    #  capture content of last brackets (...))
    pattern = re.compile(r"users:.*\(([^\(\)]*?)\)\)$")

    for ss_line in os.popen("ss -tlnp 2>/dev/null | sort -k 4").readlines():
        parts = ss_line.split()
        # Skip lines with wrong format
        if len(parts) < 6 or "users:" not in parts[5]:
            continue

        match = re.match(pattern, parts[5])
        if match is None:
            continue
        proc_info = match.group(1)
        proc, pid, _fd = proc_info.split(",")
        proc = proc.replace('"', "")
        pid = pid.replace("pid=", "")

        # Skip unwanted processes
        if proc not in procs:
            continue

        # Add only the first found port of a single server process
        if pid in pids:
            continue
        pids.append(pid)

        server_address, server_port = parse_address_and_port(parts[3])

        results.append((server_address, server_port))

    if not results:
        # if ss output was empty (maybe not installed), try netstat instead
        # (plugin silently fails without any section output,
        #  if neither netstat nor ss are installed.)

        for netstat_line in os.popen("netstat -tlnp 2>/dev/null | sort -k 4").readlines():
            parts = netstat_line.split()
            # Skip lines with wrong format
            if len(parts) < 7 or "/" not in parts[6]:
                continue

            pid, proc = parts[6].split("/", 1)
            to_replace = re.compile("^.*/")
            proc = to_replace.sub("", proc)

            # the pid/proc field length is limited to 19 chars. Thus in case of
            # long PIDs, the process names are stripped of by that length.
            # Workaround this problem here
            stripped_procs = [p[: 19 - len(pid) - 1] for p in procs]

            # Skip unwanted processes
            if proc not in stripped_procs:
                continue
            # Add only the first found port of a single server process
            if pid in pids:
                continue
            pids.append(pid)

            server_address, server_port = parse_address_and_port(parts[3])

            results.append((server_address, server_port))
            
    return results

def netcat(address, port, command):
    if ':' in address:
        if address.startswith('[') and address.endswith(']'):
            address = address[1:-1]
        s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((address, port))
    s.sendall('%s\r\n' % command)
    s.shutdown(socket.SHUT_WR)
    res = ''
    while 1:
        data = s.recv(1024)
        if data == "":
            break
        res += data
    s.close()
    return res

if instances is None:
    instances = try_detect_servers()

if not instances:
    sys.exit(0)

print '<<<memcached>>>'
for server in instances:
    if isinstance(server, tuple):
        address, port = server
    else:
        address = server['address']
        port = server['port']
    print '[%s:%s]' % (address, port)
    try:
        for line in netcat(address, port, 'stats').split('\r\n'):
            if line.startswith('STAT '):
                print line[5:]
    except Exception, e:
        sys.stderr.write('Exception (%s:%s): %s\n' % (address, port, e))
