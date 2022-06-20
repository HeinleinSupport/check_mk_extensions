#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-

# (c) 2022 Heinlein Support GmbH
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

# Example output from agent:
# <<<openvpn_clients:sep(44)>>>
# [[ovpn-instance]]
# wilhelmshilfe-hups1,84.161.206.33:58371,11267978,8134524,Sun Mar 10 14:02:27 2013
# wilhelmshilfe-hups365,84.161.206.33:59737,924198,809268,Sun Mar 10 13:59:14 2013
# wilhelmshilfe-bartenbach-redu,78.43.52.102:40411,492987861,516066364,Sun Mar 10 03:55:01 2013
# wilhelmshilfe-hups3,84.161.206.33:58512,8224815,6189879,Sun Mar 10 11:32:40 2013
# wilhelmshilfe-heiningen,46.5.209.251:3412,461581486,496901007,Fri Mar  8 10:02:38 2013
# wilhelmshilfe-hups5,84.161.206.33:60319,721646,336190,Sun Mar 10 14:23:30 2013
# wilhelmshilfe-suessen,92.198.38.212:3077,857194558,646128778,Fri Mar  8 10:02:38 2013
# wilhelmshilfe-hups6,84.161.206.33:61410,3204103,2793366,Sun Mar 10 11:59:13 2013
# wilhelmshilfe-gw-fau1,217.92.99.180:55683,109253134,96735180,Sun Mar 10 10:11:44 2013
# wilhelmshilfe-bendig,78.47.146.190:34475,5787319,19395097,Sat Mar  9 10:02:52 2013
# wilhelmshilfe-ursenwang,46.223.206.6:47299,747919254,922426625,Fri Mar  8 10:02:38 2013
# vpn-wilhelmshilfe.access.lihas.de,79.204.249.30:59046,12596972,31933023,Sun Mar 10 09:32:22 2013
# wilhelmshilfe-karlshof,92.198.38.214:3078,810996228,716994592,Fri Mar  8 10:02:39 2013

# Common Name,Real Address,Bytes Received,Bytes Sent,Connected Since

from .agent_based_api.v1.type_defs import (
    CheckResult,
    DiscoveryResult,
)

from .agent_based_api.v1 import (
    get_rate,
    get_value_store,
    register,
    render,
    Metric,
    Result,
    State,
    Service,
    )

import time

from cmk.utils import debug
from pprint import pprint

def parse_openvpn_clients(string_table):
    section = {}
    if debug.enabled():
        pprint(string_table)

    insta = 'default'
    for line in string_table:
        if line[0].startswith('[['):
            insta = line[0][2:-2]
            if insta.startswith('ovpn-'):
                insta = insta[5:]
        else:
            if insta not in section:
                section[insta] = {}
            section[insta][line[0]] = {
                'srcaddr': line[1],
                'rx': int(line[2]),
                'tx': int(line[3]),
                'since': line[4],
            }

    if debug.enabled():
        pprint(section)

    return section

def discovery_openvpn_clients(section):
    for insta in section:
        for cn in section[insta]:
            yield Service(item="%s %s" % (insta, cn))

def check_openvpn_clients(item, section):
    insta, cn = item.split(' ')
    if insta in section:
        if cn in section[insta]:
            data = section[insta][cn]
            vs = get_value_store()
            now = time.time()
            yield Result(state=State.OK,
                         summary="Channel is up")
            for what, val in [("in", data['rx']), ("out", data['tx'])]:
                bytes_per_sec = get_rate(vs, "openvpn_clients.%s.%s.%s" % (insta, cn, what), now, val)
                yield Metric(what, bytes_per_sec)
                yield Result(state=State.OK,
                             summary="%s: %s/sec" % (what, render.bytes(bytes_per_sec)))
        else:
            yield Result(state=State.OK,
                         summary="Channel is down")
    else:
        yield Result(state=State.UNKNOWN,
                     summary="Instance not found")

def cluster_openvpn_clients(item, section):
    insta, cn = item.split(' ')
    any_running = any(insta in node_section and cn in node_section[insta] for node_section in section.values())
    for node, node_section in section.items():
        if insta in node_section:
            if cn in node_section[insta]:
                yield from check_openvpn_clients(item, node_section)
    if not any_running:
        yield Result(state=State.OK,
                     summary="Channel is down")

def discovery_openvpn_instance(section):
    for insta in section:
        yield Service(item=insta)

def check_openvpn_instance(item, section):
    if item in section:
        count = len(section[item].keys())
        yield Result(state=State.OK,
                     summary="%d active users" % count)
        yield Metric("active_vpn_users", count)

def cluster_openvpn_instance(item, section):
    for node_section in section.values():
        if item in node_section:
            yield from check_openvpn_instance(item, node_section)

register.agent_section(
    name="openvpn_clients",
    parse_function=parse_openvpn_clients,
)

register.check_plugin(
    name="openvpn_clients",
    service_name="OpenVPN Client %s",
    sections=["openvpn_clients"],
    discovery_function=discovery_openvpn_clients,
    check_function=check_openvpn_clients,
    cluster_check_function=cluster_openvpn_clients,
)

register.check_plugin(
    name="openvpn_instance",
    service_name="OpenVPN Instance %s",
    sections=["openvpn_clients"],
    discovery_function=discovery_openvpn_instance,
    check_function=check_openvpn_instance,
    cluster_check_function=cluster_openvpn_instance,
)
