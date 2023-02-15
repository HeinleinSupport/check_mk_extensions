#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2023 Heinlein Consulting GmbH
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

from .agent_based_api.v1 import (
    check_levels,
    register,
    render,
    Result,
    Metric,
    State,
    Service,
)

import datetime

from cmk.utils import debug
from pprint import pprint

_siproxd_stats_map = {
    'clients_registered': 'registered Clients',
    'clients_active': 'active Clients',
    'calls_active': 'active Calls',
    'streams_active': 'active Streams',
}

def parse_siproxd_stats(string_table):
    section = {}
    if debug.enabled():
        pprint(string_table)
    for line in string_table:
        comps = line[0].split(': ')
        if len(comps) == 2:
            key = comps[0]
            value = comps[1].strip()
            if key == 'Date':
                section['dateinfo'] = datetime.datetime.strptime(value, '%a %b %d %H:%M:%S %Y')
            if key == 'PID':
                section['pid'] = int(value)
            for metric, desc in _siproxd_stats_map.items():
                if key == desc:
                    section[metric] = int(value)
    if debug.enabled():
        pprint(section)
    return section

register.agent_section(
    name="siproxd_stats",
    parse_function=parse_siproxd_stats,
)

def discover_siproxd_stats(section):
    if 'pid' in section:
        yield Service(parameters={'pid': section['pid']})

def check_siproxd_stats(params, section):
    if debug.enabled():
        pprint(params)
    if 'pid' in params and 'pid' in section:
        if params['pid'] != section['pid']:
            yield Result(state=State.CRIT,
                         summary='PID has changed')
    if 'dateinfo' in section:
        if section['dateinfo'] < datetime.datetime.now() - datetime.timedelta(minutes=10):
            yield Result(state=State.WARN,
                         summary='Stats file is from %s' % section['dateinfo'])
        else:
            yield Result(state=State.OK,
                         notice='Stats file is from %s' % section['dateinfo'])
    for key, desc in _siproxd_stats_map.items():
        if key in section:
            yield Result(state=State.OK,
                         summary='%d %s' % (section[key], desc))
            yield Metric(key, section[key])

register.check_plugin(
    name="siproxd_stats",
    service_name="Siproxd Stats",
    sections=["siproxd_stats"],
    discovery_function=discover_siproxd_stats,
    check_function=check_siproxd_stats,
    check_default_parameters={},
    # check_ruleset_name="siproxd_stats",
)
