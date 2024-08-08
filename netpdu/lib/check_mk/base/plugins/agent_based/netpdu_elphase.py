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
from cmk.plugins.lib.elphase import check_elphase

def parse_netpdu_elphase(string_table: StringTable) -> Dict[str, Dict[str, int]]:
    section = {}
    for line in string_table:
        section[line[0]] = {
            'voltage': int(line[3]),
            'energy': int(line[2]),
            'power': int(line[1]),
        }
    return section

register.snmp_section(
    name="netpdu_elphase",
    detect=contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.30966"),
    parse_function=parse_netpdu_elphase,
    fetch=SNMPTree(
            base=".1.3.6.1.4.1.30966.10.3",
            oids=[
                "1.1.0",  # name of pdu
                "2.56.0", # watt
                "2.7.0",  # watthours
                "2.1.0",  # volt
            ]),
)

def discover_netpdu_elphase(section) -> DiscoveryResult:
    for item in section:
        yield Service(item=item)

register.check_plugin(
    name='netpdu_elphase',
    sections=['netpdu_elphase'],
    service_name='Output Phase %s',
    check_default_parameters={
        'voltage': (228, 226),
        'power': (3000, 3400),
    },
    discovery_function=discover_netpdu_elphase,
    check_function=check_elphase,
    check_ruleset_name='ups_outphase',
)
