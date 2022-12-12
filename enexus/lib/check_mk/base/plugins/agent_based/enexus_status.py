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

from typing import NamedTuple

from .agent_based_api.v1 import (
    contains,
    register,
    Result,
    Service,
    SNMPTree,
    State,
)
from .agent_based_api.v1.type_defs import (
    CheckResult,
    DiscoveryResult,
)

class EnexusInfo(NamedTuple):
    status: str
    typ: str
    mode: str
    company: str
    site: str
    model: str
    serial: str
    voltage: int
    decimal: str
    temp: str
    capacity: str

def parse_enexus_status(string_table) -> EnexusInfo:
    parsed = None
    if len(string_table) == 1 and len(string_table[0]) == 1 and len(string_table[0][0]) == 11:
        parsed = EnexusInfo(*string_table[0][0])
    return parsed

register.snmp_section(
    name="enexus_status",
    parse_function=parse_enexus_status,
    fetch=[
        SNMPTree(
            base=".1.3.6.1.4.1.12148.10.2",
            oids=[
                "1.0", # SP2-MIB::powerSystemStatus
                "2.0", # SP2-MIB::powerSystemType
                "3.0", # SP2-MIB::powerSystemMode
                "4.0", # SP2-MIB::powerSystemCompany
                "5.0", # SP2-MIB::powerSystemSite
                "6.0", # SP2-MIB::powerSystemModel
                "7.0", # SP2-MIB::powerSystemSerialNumber
                "9.0", # SP2-MIB::powerSystemNominalVoltage
                "15.0", # SP2-MIB::powerSystemCurrentDecimalSetting
                "16.0", # SP2-MIB::powerSystemTemperatureScale
                "17.0", # SP2-MIB::powerSystemCapacityScale
            ],
        ),
    ],
    detect=contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.12148.10"),
)

def discover_enexus_status(section: EnexusInfo) -> DiscoveryResult:
    yield Service()

def check_enexus_status(section: EnexusInfo) -> CheckResult:
    map = {
        'status': {
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
        'typ': {
            "1": ("Smartpack 2", State.OK),
            "2": ("Smartpack S", State.OK),
            "3": ("Compack", State.OK),
        },
        'mode': {
            "0": ("off", State.CRIT),
            "1": ("test", State.WARN),
            "2": ("boost", State.WARN),
            "3": ("float", State.OK),
        },
        'decimal': {
            "0": ("Ampere", State.OK),
            "1": ("deciAmpere", State.OK),
        },
        'temp': {
            "0": ("Celsius", State.OK),
            "1": ("Fahrenheit", State.OK),
        },
        'capacity': {
            "0": ("Ah", State.OK),
            "1": ("%", State.OK),
        },
    }
    for field in section._fields:
        m = map.get(field, None)
        value = getattr(section, field)
        if m:
            text, state = m.get(value, ("unknown", State.UNKNOWN))
        else:
            text, state = value, State.OK
        yield Result(state=state, summary="%s: %s" % (field.capitalize(), text))

register.check_plugin(
    name="enexus_status",
    service_name="eNexus Status",
    discovery_function=discover_enexus_status,
    check_function=check_enexus_status,
)
