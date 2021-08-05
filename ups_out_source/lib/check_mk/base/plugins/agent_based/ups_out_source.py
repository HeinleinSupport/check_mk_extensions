#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
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

from .agent_based_api.v1 import (
    register,
    Result,
    Service,
    SNMPTree,
    State,
)
from .agent_based_api.v1.type_defs import (
    CheckResult,
    DiscoveryResult,
    StringTable,
)
from .utils.ups import DETECT_UPS_GENERIC

def parse_ups_out_source(string_table: StringTable) -> StringTable:
    if string_table:
        return { 'info': string_table[0][0] }
    return None

register.snmp_section(
    name="ups_out_source",
    detect=DETECT_UPS_GENERIC,
    parse_function=parse_ups_out_source,
    fetch=SNMPTree(
        base=".1.3.6.1.2.1.33.1.4",
        oids=["1.0"],
    ),
)

def discover_ups_out_source(section: StringTable) -> DiscoveryResult:
    yield Service()

def check_ups_out_source(section: StringTable) -> CheckResult:
    map_source = {
        "1": (State.WARN, "Other"),
        "2": (State.CRIT, "None"),
        "3": (State.OK, "Normal"),
        "4": (State.WARN, "Bypass"),
        "5": (State.CRIT, "Battery"),
        "6": (State.WARN, "Booster"),
        "7": (State.WARN, "Reducer"),
    }

    state, text = map_source.get(section['info'], (State.UNKNOWN, "Unknown"))

    yield Result(state=state,
                 summary="Output source is %s" % text)

register.check_plugin(
    name='ups_out_source',
    service_name="OUT source",
    discovery_function=discover_ups_out_source,
    check_function=check_ups_out_source,
)
