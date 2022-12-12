#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2022 Heinlein Support GmbH
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

from typing import NamedTuple, Dict

from .agent_based_api.v1 import (
    check_levels,
    contains,
    register,
    Metric,
    OIDEnd,
    Result,
    Service,
    SNMPTree,
    State,
)
from .agent_based_api.v1.type_defs import (
    CheckResult,
    DiscoveryResult,
)

class EnexusLoadfuse(NamedTuple):
    Status: str
    Description: str
    Alarm: str
    Value: str

def parse_enexus_loadfuse(string_table) -> Dict[str, EnexusLoadfuse]:
    parsed = {}
    if len(string_table) == 2:
        if len(string_table[0]) == 1:
            line = [ string_table[0][0][0], 'Total', None, None ]
            parsed['Total'] = EnexusLoadfuse(*line)
        for line in string_table[1]:
            parsed[line[0]] = EnexusLoadfuse(*line[1:])
    return parsed

register.snmp_section(
    name="enexus_loadfuse",
    parse_function=parse_enexus_loadfuse,
    fetch=[
        SNMPTree(
            base=".1.3.6.1.4.1.12148.10.9",
            oids=[
                "3.0", # SP2-MIB::loadFusesStatus
            ],
        ),
        SNMPTree(
            base=".1.3.6.1.4.1.12148.10.9.7.1",
            oids=[
                OIDEnd(),
                "1", # SP2-MIB::loadFuseStatus
                "2", # SP2-MIB::loadFuseDescription
                "4", # SP2-MIB::loadFuseAlarmEnable
                "5", # SP2-MIB::loadFuseValue
            ],
        ),
    ],
    detect=contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.12148.10"),
)

def discover_enexus_loadfuse(section: Dict[str, EnexusLoadfuse]) -> DiscoveryResult:
    for ind in section.keys():
        yield Service(item=ind)

def check_enexus_loadfuse(item, section: Dict[str, EnexusLoadfuse]) -> CheckResult:
    map = {
        'Status': {
            "0": ("error", State.CRIT),
            "1": ("normal", State.OK),
            "2": ("minorAlarm", State.WARN),
            "3": ("majorAlarm", State.CRIT),
            "4": ("disabled", State.CRIT),
            "5": ("disconnected", State.CRIT),
            "6": ("notPresent", State.UNKNOWN),
            "7": ("minorAndMajor", State.CRIT),
            "8": ("majorLow", State.CRIT),
            "9": ("minorLow", State.WARN),
            "10": ("majorHigh", State.CRIT),
            "11": ("minorHigh", State.WARN),
            "12": ("event", State.WARN),
            "13": ("valueVolt", State.OK),
            "14": ("valueAmp", State.OK),
            "15": ("valueTemp", State.OK),
            "16": ("valueUnit", State.OK),
            "17": ("valuePerCent", State.OK),
            "18": ("critical", State.CRIT),
            "19": ("warning", State.WARN),
        },
    }
    loadfuse = section.get(item)
    if loadfuse:
        for field in ['Description', 'Status']:
            m = map.get(field, None)
            value = getattr(loadfuse, field)
            if m:
                text, state = m.get(value, ("unknown", State.UNKNOWN))
            else:
                text, state = value, State.OK
            yield Result(state=state, summary="%s: %s" % (field, text))
        if loadfuse.Description != 'Total':
            yield Metric(name="fuseload", value=float(loadfuse.Value))
                                    

register.check_plugin(
    name="enexus_loadfuse",
    service_name="eNexus Load Fuse %s",
    discovery_function=discover_enexus_loadfuse,
    check_function=check_enexus_loadfuse,
)
