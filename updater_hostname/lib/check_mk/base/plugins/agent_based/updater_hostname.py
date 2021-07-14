#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2021 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  This file is distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

from .agent_based_api.v1.type_defs import (
    CheckResult,
    DiscoveryResult,
)

from .agent_based_api.v1 import (
    register,
    Result,
    State,
    Service,
    )

from cmk.base.check_api import host_name

def parse_updater_hostname(string_table):
    section = {}

    for line in string_table:
        section[line[0]] = line[1]

    return section

register.agent_section(
    name="updater_hostname",
    parse_function=parse_updater_hostname,
)

def discover_updater_hostname(section) -> DiscoveryResult:
    if 'conf' in section:
        yield Service()

def check_updater_hostname(section) -> CheckResult:
    map = { 'fqdn': 'FQDN',
            'host': 'Hostname',
            'conf': 'Updater Configuration' }
    for key, value in section.items():
        state = State.OK
        if key == 'conf' and value != host_name():
            state = State.WARN
        yield Result(state=state,
                     summary="%s: %s" % ( map[key], value ))

register.check_plugin(
    name="updater_hostname",
    service_name="Check_MK Updater Hostname",
    sections=["updater_hostname"],
    discovery_function=discover_updater_hostname,
    check_function=check_updater_hostname,
)
