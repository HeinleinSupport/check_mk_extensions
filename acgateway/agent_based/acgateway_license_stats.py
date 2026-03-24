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
    check_levels,
    contains,
    DiscoveryResult,
    render,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    StringTable,
)

def parse_acgateway_license_stats(string_table: StringTable):
    if len(string_table) == 1 and len(string_table[0]) == 6:
        section = {
            "SIP Rec": int(string_table[0][0]),
            "Transcoding": int(string_table[0][1]),
            "SBC Media": int(string_table[0][2]),
            "SBC Signaling": int(string_table[0][3]),
            "FEU": int(string_table[0][4]),
            "Web RTC": int(string_table[0][5]),
        }
    else:
        section = {}
    return section

snmp_section_acgateway_license_stats = SimpleSNMPSection(
    name = "acgateway_license_stats",
    parse_function = parse_acgateway_license_stats,
    fetch = SNMPTree(
        base = ".1.3.6.1.4.1.5003.15.2.1.1.1",
        oids = [
            "1.0", # AC-KPI-MIB::acKpiLicenseStatsCurrentGlobalLicenseSipRecUsage
            "2.0", # AC-KPI-MIB::acKpiLicenseStatsCurrentGlobalLicenseTranscodingUsage
            "3.0", # AC-KPI-MIB::acKpiLicenseStatsCurrentGlobalLicenseSbcMediaUsage
            "4.0", # AC-KPI-MIB::acKpiLicenseStatsCurrentGlobalLicenseSbcSignalingUsage
            "5.0", # AC-KPI-MIB::acKpiLicenseStatsCurrentGlobalLicenseFeuUsage
            "6.0", # AC-KPI-MIB::acKpiLicenseStatsCurrentGlobalLicenseWebRTCUsage
        ],
    ),
    detect = contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.5003.8.1.1"),
)

def discover_acgateway_license_stats(section) -> DiscoveryResult:
    for lic_id in section:
        yield Service(item=lic_id)

def check_acgateway_license_stats(item, section) -> CheckResult:
    if item in section:
        yield from check_levels(
            value=section[item],
            metric_name="license_usage",
            render_func=render.percent,
            label="Usage",
        )

check_plugin_acgateway_license_stats = CheckPlugin(
    name = "acgateway_license_stats",
    service_name = "License %s",
    discovery_function = discover_acgateway_license_stats,
    check_function = check_acgateway_license_stats,
)
