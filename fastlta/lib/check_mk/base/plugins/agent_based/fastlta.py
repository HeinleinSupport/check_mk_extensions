#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2023 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>

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

from typing import NamedTuple

from .agent_based_api.v1 import (
    all_of,
    any_of,
    check_levels,
    exists,
    register,
    render,
    startswith,
    Metric,
    OIDEnd,
    Result,
    Service,
    ServiceLabel,
    SNMPTree,
    State,
)

from .agent_based_api.v1.type_defs import (
    CheckResult,
    DiscoveryResult,
)

from cmk.utils import debug
from pprint import pprint

def parse_fastlta_silentcubes(string_table):
    section = {}
    if debug.enabled():
        pprint(string_table)
    if len(string_table) == 1:
        data = string_table[0]
        section['Disks'] = (int(data[0]), int(data[1]))
        section['PSUs'] = (int(data[2]), int(data[3]))
        section['Fans'] = (int(data[4]), int(data[5]))
    if debug.enabled():
        pprint(section)        
    return section

register.snmp_section(
    name="fastlta_silentcubes",
    parse_function=parse_fastlta_silentcubes,
    fetch=SNMPTree(
            base=".1.3.6.1.4.1.27417.3.1.1",
            oids=[
                "12.0", # 0 FAST-SILENTCUBE::scNumDisks
                "13.0", # 1 FAST-SILENTCUBE::scNumOKDisks
                "14.0", # 2 FAST-SILENTCUBE::scNumPSUs
                "15.0", # 3 FAST-SILENTCUBE::scNumOKPSUs
                "16.0", # 4 FAST-SILENTCUBE::scNumFans
                "17.0", # 5 FAST-SILENTCUBE::scNumOKFans
            ]),
    detect=all_of(
        startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.8072.3.2.10"),
        any_of(
            exists(".1.3.6.1.4.1.27417.3.2"),
            exists(".1.3.6.1.4.1.27417.3.2.0"),
        )
    ),
)

def discover_fastlta_silentcubes(section):
    for key in section:
        yield Service(item=key)

def check_fastlta_silentcubes(item, section):
    if item in section:
        data = section[item]
        yield Result(state=State.OK,
                     summary="%d %s installed" % (data[0], item))
        if data[1] != data[0]:
            yield Result(state=State.CRIT,
                         summary="only %d %s OK" % (data[1], item))

register.check_plugin(
    name="fastlta_silentcubes",
    sections=['fastlta_silentcubes'],
    service_name="Fast LTA %s",
    discovery_function=discover_fastlta_silentcubes,
    check_function=check_fastlta_silentcubes,
)
