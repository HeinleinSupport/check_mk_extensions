#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# (c) 2020 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de
#
# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# tails. You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

# .1.3.6.1.4.1.1369.6.1.1.1.0 684 --> STONESOFT-NETNODE-MIB::nodeClusterId.0
# .1.3.6.1.4.1.1369.6.1.1.2.0 1 --> STONESOFT-NETNODE-MIB::nodeMemberId.0
# .1.3.6.1.4.1.1369.6.1.1.3.0 1 --> STONESOFT-NETNODE-MIB::nodeOperState.0

from .agent_based_api.v1 import (
    contains,
    get_value_store,
    register,
    render,
    Result,
    Service,
    SNMPTree,
    State,
)

def parse_stonesoft_firewall_nodeinfo(string_table):
    section = {}
    if len(string_table) == 1 and len(string_table[0]) == 3:
        section = {
            'clusterid': string_table[0][0],
            'memberid': string_table[0][1],
            'operstate': int(string_table[0][2])
        }
    return section

register.snmp_section(
    name="stonesoft_firewall_nodeinfo",
    detect=contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.1369.5.2"),
    parse_function=parse_stonesoft_firewall_nodeinfo,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.1369.6.1.1",
        oids=[
            "1.0",
            "2.0",
            "3.0",
        ]
    ),
)

def discover_stonesoft_firewall_nodeinfo(section):
    yield Service(parameters={'operstate': section['operstate']})

def check_stonesoft_firewall_nodeinfo(params, section):
    map_operstate = {
        0: (3, 'Unknown'),
        1: (0, 'Online'),
        2: (0, 'Going Online'),
        3: (0, 'Locked Online'),
        4: (0, 'Going Locked Online'),
        5: (2, 'Offline'),
        6: (2, 'Going Offline'),
        7: (2, 'Locked Offline'),
        8: (2, 'Going Locked Offline'),
        9: (1, 'Standby'),
        10: (1, 'Going Standby'),
    }
    if 'operstate' in section:
        yield Result(state=State.OK,
                     summary="Cluster-ID: %s" % section['clusterid'])
        yield Result(state=State.OK,
                     summary="Member-ID: %s" % section['memberid'])
        prev_state = params.get('operstate', 0)
        cur_state = section['operstate']
        state = State.OK
        state_cur, text_cur = map_operstate.get(cur_state, (State.UNKNOWN, 'Unknown'))
        if prev_state != cur_state:
            state = state_cur
        yield Result(state=state,
                     summary="State: %s" % text_cur)

register.check_plugin(
    name='stonesoft_firewall_nodeinfo',
    service_name="Cluster Node",
    discovery_function=discover_stonesoft_firewall_nodeinfo,
    check_function=check_stonesoft_firewall_nodeinfo,
    check_default_parameters={},
)
