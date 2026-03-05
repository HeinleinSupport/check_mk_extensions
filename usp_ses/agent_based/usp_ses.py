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


"""
Check_MK agent_based check for USP SES (SNMP based)

Authors:    Robert Sander <r.sander@heinlein-support.de>
            Roger Ellenberger <roger.ellenberger@wagner.ch>
"""


from __future__ import annotations
from typing import Dict, NamedTuple

from cmk.agent_based.v2 import (
    CheckResult,
    DiscoveryResult,
    CheckPlugin,
    startswith,
    check_levels,
    Service,
    SimpleSNMPSection,
    SNMPTree,
)


class vHost(NamedTuple):
    """USP SES vHost"""
    index: int
    name: str
    client_connections: int
    requests_per_second: float
    active_users: int
    avg_request_time: float

    @staticmethod
    def get_vhost_by_snmp_data(line) -> vHost:
        return vHost(
            index=int(line[0]),
            name=line[1],
            client_connections=int(line[2]),
            requests_per_second=float(line[3]),
            active_users=int(line[4]),
            avg_request_time=float(line[5]),
        )


def parse_usp_ses(string_table) -> Dict[str, vHost]:
    return {line[1]: vHost.get_vhost_by_snmp_data(line) for line in string_table}


snmp_section_usp_ses = SimpleSNMPSection(
    name="usp_ses",
    detect=startswith(".1.3.6.1.2.1.1.1.0", "USP SES Appliance"),
    parse_function=parse_usp_ses,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.26458.5911.100.2.2.1",
        oids=[
            "1",  # vhostIndex
            "2",  # vhostName
            "3",  # vhostClientConnections
            "4",  # vhostRequestPerSecond
            "5",  # vhostActiveUsers
            "6",  # vhostAvgRequestTime
        ])
)


def discover_usp_ses(section) -> DiscoveryResult:
    for vhost in section.values():
        yield Service(item=vhost.name)


METRICS: Dict = {
    'client_connections': 'Client connections',
    'requests_per_second': 'Requests per second',
    'active_users': 'Active users',
    'avg_request_time': 'Average request time',
}


def check_usp_ses(item: str, params: Dict, section: Dict[str, vHost]) -> CheckResult:
    for vhost_name, vhost in section.items():
        if vhost_name == item:

            for metric_name, metric_descr in METRICS.items():
                yield from check_levels(getattr(vhost, metric_name),
                                        metric_name=metric_name,
                                        label=metric_descr,
                                        levels_upper=params.get(metric_name))
            return


check_plugin_usp_ses = CheckPlugin(
    name="usp_ses",
    service_name="USP SES vhost %s",
    discovery_function=discover_usp_ses,
    check_function=check_usp_ses,
    check_ruleset_name='usp_ses_levels',
    check_default_parameters={},
)
