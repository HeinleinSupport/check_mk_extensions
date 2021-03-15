#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

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

def parse_printer_used_ricoh(string_table):
    ricoh_unit = {
        '8': 'pages printed',
        '50': 'cartridges used',
    }

    counter = [
        'Counter: Machine Total',
        'Counter: Black & White',
        'Counter: Economy Color',
        'Counter: Full Color',
        'Cartridge Use Number: Black',
        'Cartridge Use Number: Cyan',
        'Cartridge Use Number: Magenta',
        'Cartridge Use Number: Yellow',
    ]
    section = {}
    for line in string_table[0]:
        if line[3] in counter:
            name = line[3].lower()
            color = "other"
            if "black & white" in name:
                color = "black_white"
            elif "economy" in name:
                color = "economy"
            elif "full color" in name:
                color = "full_color"
            elif "total" in name:
                color = "total"
            elif "black" in name:
                color = "black"
            elif "cyan" in name:
                color = "cyan"
            elif "magenta" in name:
                color = "magenta"
            elif "yellow" in name:
                color = "yellow"
            metric_name = "%s_%s" % ("_".join(ricoh_unit.get(line[2],
                                                             "unknown").split()),
                                     color)
            
            section[line[3]] = { 'value': int(line[7]),
                                 'title': line[4],
                                 'color': color,
                                 'unit': ricoh_unit.get(line[2], ''),
                                 'metric_name': metric_name,
            }
    return section

def discover_printer_used_ricoh(section) -> DiscoveryResult:
    for item, data in section.items():
        yield Service(item=item)

def check_printer_used_ricoh(item, section) -> CheckResult:
    if item in section:
        data = section[item]

        yield Result(state=State.OK,
                     summary="%s: %d %s" % ( data['title'],
                                             data['value'],
                                             data['unit'] ))
        yield Metric(data['metric_name'], data['value'])

register.snmp_section(
    name="printer_used_ricoh",
    parse_function=parse_printer_used_ricoh,
    fetch=[
        SNMPTree(
            base=".1.3.6.1.4.1.367.3.2.1.2.19.5.1",
            oids=[ "2", "3", "4", "5", "6", "7", "8", "9" ],
        ),
    ],
    detect=contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.367.1.1"),
)

register.check_plugin(
    name="printer_used_ricoh",
    sections=["printer_used_ricoh"],
    service_name="Ricoh %s",
    check_function=check_printer_used_ricoh,
    discovery_function=discover_printer_used_ricoh,
)
