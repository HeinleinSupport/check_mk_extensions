#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2018 Heinlein Support GmbH
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

from dataclasses import dataclass
from typing import Dict, List, Optional

from .agent_based_api.v1 import (
    contains,
    register,
    Metric,
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
from .utils.ups import (
    Battery,
)

def optional_float(value: str, *, factor: int = 1) -> Optional[float]:
    if value.strip() == "":
        return None
    return float(value.strip()) * factor

@dataclass
class GamatronicBat(Battery):
    fuse_ok: Optional[bool] = None
    current: Optional[float] = None

def parse_gamatronic_bat_status(string_table: List[StringTable]) -> Dict[str, GamatronicBat]:
    section = {}
    for line in string_table[0]:
        section[line[0]] = GamatronicBat(
            not_charging = False if line[1] == "0" else True,
            low = True if line[3] == "2" else False,
            fault = True if line[3] == "1" else False,
            fuse_ok = True if line[4] == "0" else False,
            current = optional_float(line[2], factor=0.1),
        )
    return section

register.snmp_section(
    name="gamatronic_bat_status",
    parse_function=parse_gamatronic_bat_status,
    fetch=[
        SNMPTree(
            base=".1.3.6.1.4.1.6050.1.2.26.1",
            oids=[
                "1", # psBatteryIndex
                "2", # psBatteryCurrentDirection
                "3", # psBatteryCurrent
                "6", # psBatteryStatus
                "7", # psBatteryFuseStatus
            ],
        ),
    ],
    detect=contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.6050.5"),
)

def discover_gamatronic_bat_status(section) -> DiscoveryResult:
    for item, b in section.items():
        yield Service(item=item)

def check_gamatronic_bat_status(item, section) -> CheckResult:
    if item in section:
        bat = section[item]
        if bat.not_charging:
            yield Result(state=State.WARN,
                         summary="Not Charging")
        yield Result(state=State.OK,
                     summary="Current is %0.2f A" % bat.current)
        yield Metric("current", bat.current)
        if bat.fault:
            yield Result(state=State.CRIT,
                         summary="Battery has failed")
        if bat.low:
            yield Result(state=State.WARN,
                         summary="Battery is low")
        if not bat.fuse_ok:
            yield Result(state=State.CRIT,
                         summary="Fuse is bad")

register.check_plugin(
    name="gamatronic_bat_status",
    sections=["gamatronic_bat_status"],
    service_name="Battery Status %s",
    check_function=check_gamatronic_bat_status,
    discovery_function=discover_gamatronic_bat_status,
)
