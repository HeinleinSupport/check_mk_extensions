#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2024 Heinlein Consulting GmbH
#          Robert Sander <r.sander@heinlein-support.de>

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
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    Service,
    State,
)

from datetime import datetime # pyright: ignore[reportShadowedImports]


def parse_lpar_info(string_table):
    parsed = {}
    for key, value in string_table:
        parsed[key] = value
    return parsed

agent_section_lpar_info = AgentSection(
    name="lpar_info",
    parse_function=parse_lpar_info,
)

def discover_lpar_info(section) -> DiscoveryResult:
    if 'type' in section:
        yield Service()

def check_lpar_info(section) -> CheckResult:
    yield Result(state=State.OK, summary='type: %s, ip: %s, serial: %s' % (
            section['type'],
            section['ip'],
            section['serial'],
        ))
    if section['state'] not in ['Operating']:
        yield Result(state=State.CRIT, summary='state: %s (!!)' % section['state'])

check_plugin_lpar_info = CheckPlugin(
    name="lpar_info",
    service_name="LPAR info",
    sections=["lpar_info"],
    discovery_function=discover_lpar_info,
    check_function=check_lpar_info,
)

def parse_lpar_item(string_table):
    parsed = {}
    for name, lpar_id, state, os_version, logical_serial_num, rmc_ipaddr in string_table:
        parsed[name] = {
            'id': lpar_id,
            'state': state,
            'os': os_version,
            'serial': logical_serial_num,
            'ip': rmc_ipaddr,
        }
    return parsed

agent_section_lpar_item = AgentSection(
    name="lpar_item",
    parse_function=parse_lpar_item,
)

def discover_lpar_item(section) -> DiscoveryResult:
    for name in section:
        yield Service(item=name)

def check_lpar_item(item, section) -> CheckResult:
    if item in section:
        yield Result(state=State.OK, summary='id: %s, os: %s, serial: %s' % (
            section[item]['id'],
            section[item]['os'],
            section[item]['serial'],
        ))
        if section[item]['state'] not in ['Running']:
            yield Result(state=State.CRIT, summary='state: %s (!!)' % section[item]['state'])

check_plugin_lpar_item = CheckPlugin(
    name="lpar_item",
    service_name="LPAR item %s",
    sections=["lpar_item"],
    discovery_function=discover_lpar_item,
    check_function=check_lpar_item,
)

def parse_hmc_svcevents(string_table):
    parsed = []
    for line in string_table:
        data = {}
        key = None
        for elem in line:
            if elem[0] != " " and "=" in elem:
                splitted = elem.split("=", 1)
                key = splitted[0]
                if len(splitted) == 2:
                    data[key] = splitted[1]
                else:
                    data[key] = None
            else:
                data[key] += "," + elem
        for key, value in data.items():
            if key.endswith('_time'):
                data[key] = datetime.strptime(value, '%m/%d/%Y %H:%M:%S %Z')
        parsed.append(data)
    return parsed

agent_section_hmc_svcevents = AgentSection(
    name="hmc_svcevents",
    parse_function=parse_hmc_svcevents,
)

def discover_hmc_svcevents(section) -> DiscoveryResult:
    yield Service()

def check_hmc_svcevents(section) -> CheckResult:
    if len(section) == 0:
        yield Result(state=State.OK, summary='No events available')
    else:
        for event in section:
            state=State.OK
            if event["status"] == "Open":
                state=State.WARN
            yield Result(state=state,
                         summary="Event Time: %s, Refcode: %s, Text: %s" % (
                             event["event_time"],
                             event["refcode"],
                             event["text"],
                         ))                

check_plugin_hmc_svcevents = CheckPlugin(
    name="hmc_svcevents",
    service_name="HMC Events",
    sections=["hmc_svcevents"],
    discovery_function=discover_hmc_svcevents,
    check_function=check_hmc_svcevents,
)
