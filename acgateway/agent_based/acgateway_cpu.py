#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2026 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>

#
# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    contains,
    DiscoveryResult,
    get_value_store,
    OIDEnd,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    StringTable,
)
from cmk.plugins.lib.cpu_util import check_cpu_util
import time


def parse_acgateway_cpus(string_table: StringTable):
    section = {}
    for cpu_id, value in string_table:
        section[cpu_id] = int(value)
    return section

snmp_section_acgateway_cpus = SimpleSNMPSection(
    name = "acgateway_cpus",
    parse_function = parse_acgateway_cpus,
    fetch = SNMPTree(
        base = ".1.3.6.1.4.1.5003.15.2.4.1.2.1.1",
        oids = [
            OIDEnd(),
            "2",
        ],
    ),
    detect = contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.5003.8.1.1"),
)

def discover_acgateway_cpus(section) -> DiscoveryResult:
    for cpu_id in section:
        yield Service(item=cpu_id)

def check_acgateway_cpus(item, params, section) -> CheckResult:
    if item in section:
        yield from check_cpu_util(
            util=section[item],
            params=params,
            value_store=get_value_store(),
            this_time=time.time(),
        )

check_plugin_acgateway_cpus = CheckPlugin(
    name = "acgateway_cpus",
    service_name = "CPU %s Utilization",
    discovery_function = discover_acgateway_cpus,
    check_function = check_acgateway_cpus,
    check_ruleset_name = "cpu_utilization_multiitem",
    check_default_parameters={},
)
