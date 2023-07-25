#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2021 Heinlein Support GmbH
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

import json
import rados
import os, os.path
import subprocess
import socket

class RadosCMD(rados.Rados):
    def command_mon(self, cmd, params=None):
        data = {'prefix': cmd, 'format': 'json'}
        if params:
            data.update(params)
        return self.mon_command(json.dumps(data), b'', timeout=5)
    def command_mgr(self, cmd):
        return self.mgr_command(json.dumps({'prefix': cmd, 'format': 'json'}), b'', timeout=5)
    def command_osd(self, osdid, cmd):
        return self.osd_command(osdid, json.dumps({'prefix': cmd, 'format': 'json'}), b'', timeout=5)
    def command_pg(self, pgid, cmd):
        return self.pg_command(pgid, json.dumps({'prefix': cmd, 'format': 'json'}), b'', timeout=5)

ceph_config='/etc/ceph/ceph.conf'
ceph_client='client.admin'
try:
    with open(os.path.join(os.environ['MK_CONFDIR'], 'ceph.cfg'), 'r') as config:
        for line in config.readlines():
            if '=' in line:
                key, value = line.strip().split('=')
                if key == 'CONFIG':
                    ceph_config = value
                if key == 'CLIENT':
                    ceph_client = value
except FileNotFoundError:
    pass

cluster = RadosCMD(conffile=ceph_config, name=ceph_client)
cluster.connect()

hostname = socket.gethostname().split('.', 1)[0]
fqdn = socket.getfqdn()

res = cluster.command_mon("status")
if res[0] == 0:
    status = json.loads(res[1])
    mons = status.get('quorum_names', [])
    fsid = status.get("fsid", "")

    if hostname in mons or fqdn in mons:
    # only on MON hosts

        print("<<<cephstatus:sep(0)>>>")
        print(json.dumps(status))

        res = cluster.command_mon("df", params={'detail': 'detail'})
        if res[0] == 0:
            print("<<<cephdf:sep(0)>>>")
            print(json.dumps(json.loads(res[1])))

localosds = []
res = cluster.command_mon("osd metadata")
if res[0] == 0:
    print("<<<cephosdbluefs:sep(0)>>>")
    out = {'end': {}}
    for osd in json.loads(res[1]):
        if osd.get('hostname') in [hostname, fqdn]:
            localosds.append(osd['id'])
            if "container_hostname" in osd:
                adminsocket = "/run/ceph/%s/ceph-osd.%d.asok" % (fsid, osd['id'])
            else:
                adminsocket = "/run/ceph/ceph-osd.%d.asok" % osd['id']
            if os.path.exists(adminsocket):
                chunks = []
                try:
                    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                    sock.connect(adminsocket)
                    sock.sendall(b'{"prefix": "perf dump"}\n')
                    sock.shutdown(socket.SHUT_WR)
                    while len(chunks) == 0 or chunks[-1] != b'':
                        chunks.append(sock.recv(4096))
                    sock.close()
                    chunks[0] = chunks[0][4:]
                except:
                    chunks = [b'{"bluefs": {}}']
                out[osd['id']] = {'bluefs': json.loads(b"".join(chunks))['bluefs']}
    print(json.dumps(out))

osddf_raw = cluster.command_mon("osd df")
osdperf_raw = cluster.command_mon("osd perf")
if osddf_raw[0] == 0 and osdperf_raw[0] == 0:
    osddf = json.loads(osddf_raw[1])
    osdperf = json.loads(osdperf_raw[1])
    osds = []
    for osd in osddf['nodes']:
        if osd['id'] in localosds:
            osds.append(osd)
    summary = osddf['summary']
    perfs = []
    if 'osd_perf_infos' in osdperf:
        for osd in osdperf['osd_perf_infos']:
            if osd['id'] in localosds:
                perfs.append(osd)
    if 'osdstats' in osdperf and 'osd_perf_infos' in osdperf['osdstats']:
        for osd in osdperf['osdstats']['osd_perf_infos']:
            if osd['id'] in localosds:
                perfs.append(osd)

    print("<<<cephosd:sep(0)>>>")
    out = {'df': {'nodes': osds},
           'perf': {'osd_perf_infos': perfs}}
    print(json.dumps(out))
