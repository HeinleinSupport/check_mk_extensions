#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2020 Heinlein Support GmbH
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
    render,
    Result,
    Metric,
    State,
    check_levels,
    ServiceLabel,
    Service,
)

def _hpsa_make_key(controller, key, line):
    description = {'array': 'Array',
                   'logicaldrive': 'Logical Drive',
                   'physicaldrive': 'Physical Drive'}
    return "%s %s %s" % (controller, description[key], line[1])

def parse_hpsa(string_table):
    section = {'array': {}, 'logicaldrive': {}, 'physicaldrive': {}}
    currentarray = None
    controller = None
    for line in string_table:
        if line[0] == u'Smart' and line[1] == u'Array':
            controller = " ".join(line[0:6])
        for key in section:
            if line[0].lower() == key:
                section[key][_hpsa_make_key(controller, key, line)] = {'info': (" ".join(line[2:]))[1:-1].split(', ')}
                if key == 'array':
                    currentarray = _hpsa_make_key(controller, key, line)
                if currentarray:
                    section[key][_hpsa_make_key(controller, key, line)]['array'] = currentarray
        if " ".join(line) == "HP RAID check tool not installed.":
            section['not_installed'] = True
    return section

register.agent_section(
    name="hpsa",
    parse_function=parse_hpsa,
)

def discover_hpsa(section):
    if 'not_installed' in section:
        yield Service()

def check_hpsa(section):
    yield Result(state=State.WARN,
                 summary='HP RAID Tool not installed. Please install ssacli, hpssacli or hpacucli.')

register.check_plugin(
    name="hpsa",
    service_name="HP Raid Tool",
    sections=["hpsa"],
    discovery_function=discover_hpsa,
    check_function=check_hpsa,
)

def discover_hpsa_array(section):
    for array, data in section['array'].items():
        yield Service(item=array)

def check_hpsa_array(item, section):
    if item in section['array']:
        data = section['array'][item]
        yield Result(state=State.OK,
                     summary=", ".join(data['info']))

register.check_plugin(
    name="hpsa_array",
    service_name="HP RAID %s",
    sections=["hpsa"],
    discovery_function=discover_hpsa_array,
    check_function=check_hpsa_array,
)

def discover_hpsa_logicaldrive(section):
    for ld, data in section['logicaldrive'].items():
        yield Service(item=ld)

def check_hpsa_logicaldrive(item, section):
    if item in section['logicaldrive']:
        data = section['logicaldrive'][item]
        state = State.OK
        if data['info'][2] != 'OK':
            state = State.CRIT
        yield Result(state=state,
                     summary=(' '.join(data['info'])) + ", Array " + data['array'])

register.check_plugin(
    name="hpsa_logicaldrive",
    service_name="HP RAID %s",
    sections=["hpsa"],
    discovery_function=discover_hpsa_logicaldrive,
    check_function=check_hpsa_logicaldrive,
)

def discover_hpsa_physicaldrive(section):
    for pd, data in section['physicaldrive'].items():
        yield Service(item=pd)

def check_hpsa_physicaldrive(item, section):
    if item in section['physicaldrive']:
        data = section['physicaldrive'][item]
        state = State.OK
        if data['info'][3] != 'OK':
            state = State.CRIT
        yield Result(state=state,
                     summary=(' '.join(data['info'])) + ", Array " + data['array'])

register.check_plugin(
    name="hpsa_physicaldrive",
    service_name="HP RAID %s",
    sections=["hpsa"],
    discovery_function=discover_hpsa_physicaldrive,
    check_function=check_hpsa_physicaldrive,
)
