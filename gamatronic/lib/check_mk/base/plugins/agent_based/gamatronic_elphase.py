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

from typing import Dict, List
from .agent_based_api.v1 import (
    contains,
    register,
    Metric,
    Result,
    SNMPTree,
    Service,
    State,
)
from .agent_based_api.v1.type_defs import (
    StringTable,
    CheckResult,
    DiscoveryResult,
)
from cmk.base.check_legacy_includes.elphase import check_elphase

def parse_gamatronic_phase(string_table: List[StringTable]) -> Dict[str, Dict[str, int]]:
    section = {}
    for line in string_table[0]:
        section[line[0]] = {
            'voltage': int(line[1]),
            'current': int(line[2]),
            'power': int(line[3]) * 100,
            'appower': int(line[4]) * 100,
        }
    return section

register.snmp_section(
    name="gamatronic_in_phase",
    detect=contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.6050.5"),
    parse_function=parse_gamatronic_phase,
    fetch=[
        SNMPTree(
            base=".1.3.6.1.4.1.6050.5.4.1.1",
            oids=[
                "1",
                "2", # InputVoltage
                "3", # InputCurrent
                "4", # InputAcPower
                "5", # InputApPower
            ]),
    ],
)

register.snmp_section(
    name="gamatronic_out_phase",
    detect=contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.6050.5"),
    parse_function=parse_gamatronic_phase,
    fetch=[
        SNMPTree(
            base=".1.3.6.1.4.1.6050.5.5.1.1",
            oids=[
                "1",
                "2", # InputVoltage
                "3", # InputCurrent
                "4", # InputAcPower
                "5", # InputApPower
            ]),
    ],
)

def discover_gamatronic_phase(section) -> DiscoveryResult:
    for item in section:
        yield Service(item=item)

def check_gamatronic_phase(item, params, section) -> CheckResult:
    for state, text, perfdata in check_elphase(item, params, section):
        yield Result(state=State(state), summary=text)
        for p in perfdata:
            if len(p) == 4:
                yield Metric(p[0], p[1], levels=(p[2], p[3]))
            else:
                yield Metric(p[0], p[1])

register.check_plugin(
    name='gamatronic_in_phase',
    sections=['gamatronic_in_phase'],
    service_name='UPS Input Phase %s',
    check_default_parameters={},
    discovery_function=discover_gamatronic_phase,
    check_function=check_gamatronic_phase,
    check_ruleset_name='el_inphase',
)

register.check_plugin(
    name='gamatronic_out_phase',
    sections=['gamatronic_out_phase'],
    service_name='UPS Output Phase %s',
    check_default_parameters={},
    discovery_function=discover_gamatronic_phase,
    check_function=check_gamatronic_phase,
    check_ruleset_name='ups_outphase',
)
