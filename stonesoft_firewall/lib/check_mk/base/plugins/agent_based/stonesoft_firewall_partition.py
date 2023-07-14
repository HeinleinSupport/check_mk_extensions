#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2020 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>

#
# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

#
# Total Capacity as filesystem check
#

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

from .utils import df

def parse_stonesoft_firewall_partition(string_table):
    section = {}
    for line in string_table:
        section[line[1]] = {
            'device': line[0],
            'size': int(line[2]) / 1024.0,
            'avail': int(line[3]) / 1024.0,
        }
    return section

register.snmp_section(
    name="stonesoft_firewall_partition",
    detect=contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.1369.5.2"),
    parse_function=parse_stonesoft_firewall_partition,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.1369.5.2.1.11.3.1",
        oids=[
            '2', # fwPartitionDevName
            '3', # fwMountPointName
            '4', # fwPartitionSize
            '6', # fwPartitionAvail
        ]
    ),
)

def discover_stonesoft_firewall_partition(section):
    for mp in section:
        yield Service(item=mp)

def check_stonesoft_firewall_partition(item, params, section):
    if item in section:
        vs = get_value_store()
        yield from df.df_check_filesystem_single(
            vs,
            item,
            section[item]['size'],
            section[item]['avail'],
            0,
            None,
            None,
            params=params,
        )

register.check_plugin(
    name='stonesoft_firewall_partition',
    service_name="Filesystem %s",
    discovery_function=discover_stonesoft_firewall_partition,
    check_function=check_stonesoft_firewall_partition,
    check_ruleset_name='filesystem',
    check_default_parameters=df.FILESYSTEM_DEFAULT_PARAMS,
)
