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

class GamatronicInfo(NamedTuple):
    manufacture: str
    sysname: str
    batterytype: str
    pstype: str
    controllertype: str
    serial: str

def parse_gamatronic_info(string_table) -> GamatronicInfo:
    parsed = None
    if len(string_table) == 1 and len(string_table[0]) == 1 and len(string_table[0][0]) == 6:
        parsed = GamatronicInfo(*string_table[0][0])
    return parsed

register.snmp_section(
    name="gamatronic_info",
    parse_function=parse_gamatronic_info,
    fetch=[
        SNMPTree(
            base=".1.3.6.1.4.1.6050.1.1",
            oids=[
                "2.0", # psUnitManufacture
                "1.0", # psUnitSysName
                "3.0", # psUnitBatteryType
                "4.0", # psUnitPSType
                "5.0", # psUnitControllerType
                "8.0", # psUnitSerialNumber
            ],
        ),
    ],
    detect=contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.6050.5"),
)


def discover_gamatronic_info(section: GamatronicInfo) -> DiscoveryResult:
    yield Service()

def check_gamatronic_info(section: GamatronicInfo) -> CheckResult:
    yield Result(state=State.OK,
                 summary=f"{section.manufacture} {section.sysname}, Battery: {section.batterytype} {section.pstype}, Controller: {section.controllertype}, Serial: {section.serial}")

register.check_plugin(
    name="gamatronic_info",
    service_name="Gamatronic Info",
    discovery_function=discover_gamatronic_info,
    check_function=check_gamatronic_info,
)
