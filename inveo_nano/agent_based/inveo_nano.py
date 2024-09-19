#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2024 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de
#
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

from cmk.agent_based.v2 import (
    check_levels,
    CheckPlugin,
    CheckResult,
    contains,
    DiscoveryResult,
    Metric,
    render,
    OIDEnd,
    Result,
    Service,
    SNMPSection,
    SNMPTree,
    State,
    StringTable,
)

from cmk.plugins.lib import temperature

def parse_inveo_nano(string_table: StringTable):
    section = {}
    if len(string_table) == 2:
        info, temp = string_table
        section = {
            'info': 'Name: %s, Version: %s, Date: %s' % ( info[0][0],
                                                          info[0][1],
                                                          info[0][2] ),
            'temp': int(temp[0][0])/10.0,
        }
    return section

snmp_section_inveo_nano = SNMPSection(
    name="inveo_nano",
    detect=contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.42814.14"),
    parse_function=parse_inveo_nano,
    fetch=[
        SNMPTree(
            base=".1.3.6.1.4.1.42814.14.1",
            oids=[
                "1.0",      # Nano::name
                "2.0",      # Nano::version
                "3.0",      # Nano::date
            ]),
        SNMPTree(
            base=".1.3.6.1.4.1.42814.14.3",
            oids=[
                # "1.1.0",        # Nano::ch1-on
                # "2.1.0",        # Nano::ch1-out
                # "3.1.0",        # Nano::ch1-in
                # "4.1.0",        # Nano::ch1-cnt
                "5.3.0",        # Nano::ch1-temp
            ]),
    ],
)

#.
#   .--info----------------------------------------------------------------.
#   |                          _        __                                 |
#   |                         (_)_ __  / _| ___                            |
#   |                         | | '_ \| |_ / _ \                           |
#   |                         | | | | |  _| (_) |                          |
#   |                         |_|_| |_|_|  \___/                           |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'

def discover_inveo_nano_info(section):
    if 'info' in section:
        yield Service()

def check_inveo_nano_info(section):
    if 'info' in section:
        yield Result(state=State.OK,
                     summary=section['info'])

check_plugin_inveo_nano_info = CheckPlugin(
    name="inveo_nano_info",
    sections=['inveo_nano'],
    service_name="Inveo Nano Info",
    discovery_function=discover_inveo_nano_info,
    check_function=check_inveo_nano_info,
)

#.
#   .--temperature---------------------------------------------------------.
#   |      _                                      _                        |
#   |     | |_ ___ _ __ ___  _ __   ___ _ __ __ _| |_ _   _ _ __ ___       |
#   |     | __/ _ \ '_ ` _ \| '_ \ / _ \ '__/ _` | __| | | | '__/ _ \      |
#   |     | ||  __/ | | | | | |_) |  __/ | | (_| | |_| |_| | | |  __/      |
#   |      \__\___|_| |_| |_| .__/ \___|_|  \__,_|\__|\__,_|_|  \___|      |
#   |                       |_|                                            |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'

def discover_inveo_nano_temp(section):
    if 'temp' in section:
        yield Service(item='Temp')

def check_inveo_nano_temp(item, params, section):
    if 'temp' in section:
        yield from temperature.check_temperature(
            section['temp'],
            params,
        )

check_plugin_inveo_nano_temp = CheckPlugin(
    name="inveo_nano_temp",
    sections=['inveo_nano'],
    service_name="Inveo Nano %s",
    discovery_function=discover_inveo_nano_temp,
    check_function=check_inveo_nano_temp,
    check_default_parameters={},
    check_ruleset_name="temperature",
)
