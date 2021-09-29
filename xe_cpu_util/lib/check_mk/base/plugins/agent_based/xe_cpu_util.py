#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2018 Heinlein Support GmbH
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

from cmk.utils import debug
from pprint import pprint

def parse_xe_cpu_util(string_table):
    section = {}
    if debug.enabled():
        pprint(string_table)
    for cpuid, uuid, value in string_table:
        section[int(cpuid)] = round(float(value) * 100.0, 1)
    if debug.enabled():
        pprint(section)
    return section

register.agent_section(
    name="xe_cpu_util",
    parse_function=parse_xe_cpu_util,
)

def discover_xe_cpu_util(section):
    if len(section) > 0:
        yield Service()

def check_xe_cpu_util(params, section):
    if debug.enabled():
        pprint(params)
    average = sum(section.values()) / len(section)
    perfdata = [  ]
    if 'util' in params:
        yield from check_levels(average,
                                levels_upper=params['util'],
                                boundaries=(0, 100),
                                metric_name="cpu_util_guest",
                                label="Average CPU utilisation",
                                render_func=render.percent)
    else:
        yield Metric('cpu_util_guest', average)
        yield Result(state=State.OK, summary='Average CPU utilisation: %s' % render.percent(average))
    if 'levels_single' or 'core_util_graph' in params:
        for cpuid in sorted(section.keys()):
            if 'levels_single' in params:
                yield from check_levels(section[cpuid],
                                        levels_upper=params['levels_single'],
                                        boundaries=(0, 100),
                                        metric_name='cpu_core_util_%s' % cpuid,
                                        label='Core %d' % cpuid,
                                        render_func=render.percent)
            elif 'core_util_graph' in params:
                yield Metric('cpu_core_util_%s' % cpuid, cpus[cpuid])

register.check_plugin(
    name="xe_cpu_util",
    service_name="Xen CPU Utilisation",
    sections=["xe_cpu_util"],
    discovery_function=discover_xe_cpu_util,
    check_function=check_xe_cpu_util,
    check_default_parameters={},
    check_ruleset_name="xe_cpu_util",
)
