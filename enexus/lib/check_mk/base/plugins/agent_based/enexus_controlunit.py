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

class EnexusControlUnit(NamedTuple):
    Description: str
    Status: str
    Serial: str
    HWPart: str
    HWVersion: str
    SWPart: str
    SWVersion: str

def parse_enexus_controlunit(string_table) -> Dict[str, EnexusControlUnit]:
    parsed = {}
    for line in string_table[0]:
        parsed[line[0]] = EnexusControlUnit(*line[1:])
    return parsed

register.snmp_section(
    name="enexus_controlunit",
    parse_function=parse_enexus_controlunit,
    fetch=[
        SNMPTree(
            base=".1.3.6.1.4.1.12148.10.13.8.2.1",
            oids=[
                OIDEnd(),
                "2", # SP2-MIB::controlUnitDescription
                "3", # SP2-MIB::controlUnitStatus
                "4", # SP2-MIB::controlUnitSerialNumber
                "5", # SP2-MIB::controlUnitHwPartNumber
                "6", # SP2-MIB::controlUnitHwVersion
                "7", # SP2-MIB::controlUnitSwPartNumber
                "8", # SP2-MIB::controlUnitSwVersion
            ],
        ),
    ],
    detect=contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.12148.10"),
)

def discover_enexus_controlunit(section: Dict[str, EnexusControlUnit]) -> DiscoveryResult:
    for ind in section.keys():
        yield Service(item=ind)

def check_enexus_controlunit(item, section: Dict[str, EnexusControlUnit]) -> CheckResult:
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
    cu = section.get(item)
    if cu:
        for field in cu._fields:
            m = map.get(field, None)
            value = getattr(cu, field)
            if m:
                text, state = m.get(value, ("unknown", State.UNKNOWN))
            else:
                text, state = value, State.OK
            yield Result(state=state, summary="%s: %s" % (field, text))

register.check_plugin(
    name="enexus_controlunit",
    service_name="eNexus Control Unit %s",
    discovery_function=discover_enexus_controlunit,
    check_function=check_enexus_controlunit,
)
