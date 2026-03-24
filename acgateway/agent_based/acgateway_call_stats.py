#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2026 Heinlein Support GmbH
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

from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    check_levels,
    contains,
    DiscoveryResult,
    render,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    StringTable,
)

from cmk.ccc import debug
from pprint import pprint

_metric_map = {
    "Average Call Duration": ("average_call_duration", render.timespan, "Call Duration"),
    "Active Calls In": ("active_calls", None, "Incoming Calls"),
    "Active Calls Out": ("active_calls", None, "Outgoing Calls"),
    "Active Sessions": ("sessions", None, "Sessions"),
}

def parse_acgateway_call_stats(string_table: StringTable):
    if debug.enabled:
        pprint(string_table)
    if len(string_table) == 1 and len(string_table[0]) == len(_metric_map):
        section = {
            "Average Call Duration": int(string_table[0][0]),
            "Active Calls In": int(string_table[0][1]),
            "Active Calls Out": int(string_table[0][2]),
            "Active Sessions": int(string_table[0][3]),
        }
    else:
        section = {}
    if debug.enabled():
        pprint(section)
    return section

snmp_section_acgateway_call_stats = SimpleSNMPSection(
    name = "acgateway_call_stats",
    parse_function = parse_acgateway_call_stats,
    fetch = SNMPTree(
        base=".1.3.6.1.4.1.5003.15.3.1.1.1",
        oids=[
            "1.0",  # AC-KPI-MIB::acKpiSbcCallStatsCurrentGlobalAverageCallDuration
            "2.0",  # AC-KPI-MIB::acKpiSbcCallStatsCurrentGlobalActiveCallsIn
            "3.0",  # AC-KPI-MIB::acKpiSbcCallStatsCurrentGlobalActiveCallsOut
            "43.0", # AC-KPI-MIB::acKpiSbcCallStatsCurrentGlobalActiveSessions
        ]
    ),
    detect = contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.5003.8.1.1"),
)

def discover_acgateway_call_stats(section) -> DiscoveryResult:
    for stat_id in section:
        yield Service(item=stat_id)

def check_acgateway_call_stats(item, section) -> CheckResult:
    if item in section:
        yield from check_levels(
            value=section[item],
            metric_name=_metric_map[item][0],
            render_func=_metric_map[item][1],
            label=_metric_map[item][2],
        )

check_plugin_acgateway_call_stats = CheckPlugin(
    name = "acgateway_call_stats",
    service_name = "SBC Stats %s",
    discovery_function = discover_acgateway_call_stats,
    check_function = check_acgateway_call_stats,
)
