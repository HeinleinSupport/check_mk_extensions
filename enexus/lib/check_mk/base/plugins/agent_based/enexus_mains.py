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

class EnexusMains(NamedTuple):
    Status: str
    Description: str
    Alarm: str
    Value: str
    MajorHigh: str
    MinorHigh: str
    MinorLow: str
    MajorLow: str

def parse_enexus_mains(string_table) -> Dict[str, EnexusMains]:
    parsed = {}
    if len(string_table) == 2:
        if len(string_table[0]) == 1:
            line = [ string_table[0][0][0], 'Total', '1', '0', '0', '0', '0', '0' ]
            parsed['Total'] = EnexusMains(*line)
        for line in string_table[1]:
            parsed[line[0]] = EnexusMains(*line[1:])
    return parsed

register.snmp_section(
    name="enexus_mains",
    parse_function=parse_enexus_mains,
    fetch=[
        SNMPTree(
            base=".1.3.6.1.4.1.12148.10.3",
            oids=[
                "1.0", # SP2-MIB::mainsStatus
            ],
        ),
        SNMPTree(
            base=".1.3.6.1.4.1.12148.10.3.4.1",
            oids=[
                OIDEnd(),
                "2", # SP2-MIB::mainsVoltageStatus
                "3", # SP2-MIB::mainsVoltageDescription
                "5", # SP2-MIB::mainsVoltageAlarmEnable
                "6", # SP2-MIB::mainsVoltageValue
                "7", # SP2-MIB::mainsVoltageMajorHighLevel
                "8", # SP2-MIB::mainsVoltageMinorHighLevel
                "9", # SP2-MIB::mainsVoltageMinorLowLevel
                "10", # SP2-MIB::mainsVoltageMajorLowLevel
            ],
        ),
    ],
    detect=contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.12148.10"),
)

def discover_enexus_mains(section: Dict[str, EnexusMains]) -> DiscoveryResult:
    for ind in section.keys():
        yield Service(item=ind)

def check_enexus_mains(item, section: Dict[str, EnexusMains]) -> CheckResult:
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
    mains = section.get(item)
    if mains:
        for field in ['Status', 'Description']:
            m = map.get(field, None)
            value = getattr(mains, field)
            if m:
                text, state = m.get(value, ("unknown", State.UNKNOWN))
            else:
                text, state = value, State.OK
            yield Result(state=state, summary="%s: %s" % (field, text))
        if mains.Description != 'Total':
            yield from check_levels(
                value=float(mains.Value),
                levels_upper=(float(mains.MinorHigh), float(mains.MajorHigh)),
                levels_lower=(float(mains.MinorLow), float(mains.MajorLow)),
                metric_name="voltage",
                render_func=lambda x: "%dV" % x,
                label="Voltage",
            )
                                    

register.check_plugin(
    name="enexus_mains",
    service_name="eNexus Mains %s",
    discovery_function=discover_enexus_mains,
    check_function=check_enexus_mains,
)
