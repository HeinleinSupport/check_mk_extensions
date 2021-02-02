#!/usr/bin/python3
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

from typing import Any, Dict, List, Tuple, Optional

from .utils.temperature import (
    check_temperature,
)

from .agent_based_api.v1 import (
    contains,
    register,
    SNMPTree,
    Service,
    Result,
    State,
)

from .agent_based_api.v1.type_defs import (
    StringTable,
    CheckResult,
    DiscoveryResult,
)

def parse_gamatronic_bat_temp(string_table: List[StringTable]):
    section = {}
    for line in string_table[0]:
        factor = 1.0
        if line[1] == "1":
            factor = -1.0
        section[line[0]] = float(line[2]) * factor
    return section

def discover_gamatronic_bat_temp(section) -> DiscoveryResult:
    for bat, temp in section.items():
        yield Service(item=bat)

def check_gamatronic_bat_temp(item, params, section) -> CheckResult:
    if item in section:
        yield from check_temperature(section[item],
                                     params,
                                     unique_name="ups_bat_temp_%s" % item)

register.snmp_section(
    name="gamatronic_bat_temp",
    detect=contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.6050.5"),
    parse_function=parse_gamatronic_bat_temp,
    fetch=[
        SNMPTree(
            base=".1.3.6.1.4.1.6050.1.2.26.1",
            oids=[
                "1", # psBatteryIndex
                "4", # psBatteryTemperatureSign
                "5", # psBatteryTemperature
            ]),
    ],
)

register.check_plugin(
    name='gamatronic_bat_temp',
    sections=['gamatronic_bat_temp'],
    service_name='Temperature Battery %s',
    check_default_parameters={ "levels": (40, 50) },
    discovery_function=discover_gamatronic_bat_temp,
    check_function=check_gamatronic_bat_temp,
    check_ruleset_name='temperature',
)
