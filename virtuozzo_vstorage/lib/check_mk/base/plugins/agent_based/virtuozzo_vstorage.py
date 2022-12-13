#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2022 Heinlein Support GmbH
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

def parse_virtuozzo_vstorage(string_table):
    section = {}
    for line in string_table:
        if len(line) == 4:
            section[line[0]] = {
                'status': line[1],
                'size': int(line[2]) / 1024.0 / 1024.0,
                'avail': int(line[3]) / 1024.0 / 1024.0,
            }
    return section

register.snmp_section(
    name="virtuozzo_vstorage",
    detect=contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.8072.3.2.10"),
    parse_function=parse_virtuozzo_vstorage,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.8072.161.1.1",
        oids=[
            '1.0', # Cluster Name
            '2.0', # Cluster Status
            '4.0', # Total Space
            '5.0', # Free Space
        ]
    ),
)

def discover_virtuozzo_vstorage(section):
    for mp in section:
        yield Service(item=mp)

def check_virtuozzo_vstorage(item, params, section):
    if item in section:
        vs = get_value_store()
        if section[item]['status'] != 'healthy':
            yield Result(state=State.CRIT,
                         summary="Status is %s" % section[item]['status'])
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
    name='virtuozzo_vstorage',
    service_name="Filesystem %s",
    discovery_function=discover_virtuozzo_vstorage,
    check_function=check_virtuozzo_vstorage,
    check_ruleset_name='filesystem',
    check_default_parameters=df.FILESYSTEM_DEFAULT_LEVELS,
)
