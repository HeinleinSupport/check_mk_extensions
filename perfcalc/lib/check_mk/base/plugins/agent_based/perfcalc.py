#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2019 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>
#

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
    check_levels,
    check_levels_predictive,
    get_rate,
    get_value_store,
    register,
    Metric,
    Result,
    State,
    Service,
    )

from cmk.utils import debug
from pprint import pprint

def parse_perfcalc(string_table):
    section = []
    service = False
    for line in string_table:
        if line[0] == 'service':
            service = {'description': " ".join(line[1:]),
                       'hosts': [],
                       'data': {}}
            section.append(service)
        if line[0] == 'host':
            service['hosts'] = line[1:]
        if line[0] == 'ds':
            service['data'][line[1]] = float(line[2])
    return section

register.agent_section(
    name="perfcalc",
    parse_function=parse_perfcalc,
)

def discover_perfcalc(section) -> DiscoveryResult:
    for service in section:
        yield Service(item=service['description'])

def check_perfcalc(item, params, section) -> CheckResult:
    levels = {}
    if isinstance(params, list):
        for param in params:
            if param['levels']:
                levels[param['dsname']]['upper'] = param['levels']
    else:
        for param in params.get('list', []):
            if param.get('levels'):
                levels.setdefault(param['dsname'], {})
                if isinstance(param['levels'], tuple):
                    levels[param['dsname']]['upper'] = param['levels']
                else:
                    levels[param['dsname']]['predictive'] = param['levels']
            if param.get('levels_lower'):
                levels.setdefault(param['dsname'], {})
                if isinstance(param['levels_lower'], tuple):
                    levels[param['dsname']]['lower'] = param['levels_lower']
    if debug.enabled():
        pprint(params)
        pprint(levels)

    for service in section:
        if item == service['description']:
            if service['hosts'] == []:
                yield Result(state=State.UNKNOWN,
                             summary="No matching hosts found")
            else:
                yield Result(state=State.OK,
                             notice='Data from %s' % ', '.join(service['hosts']))
            for dsname, value in service['data'].items():
                if dsname in levels:
                    if 'predictive' in levels[dsname]:
                        yield from check_levels_predictive(value,
                                                           levels=levels[dsname]['predictive'],
                                                           metric_name=dsname,
                                                           label=dsname)
                    else:
                        yield from check_levels(value,
                                                levels_upper=levels[dsname].get('upper'),
                                                levels_lower=levels[dsname].get('lower'),
                                                metric_name=dsname,
                                                label=dsname)
                else:
                    yield Result(state=State.OK,
                                 summary='%s: %s' % (dsname, value))
                    yield Metric(dsname, value)

register.check_plugin(
    name="perfcalc",
    service_name="%s",
    sections=["perfcalc"],
    discovery_function=discover_perfcalc,
    check_function=check_perfcalc,
    check_default_parameters={},
    check_ruleset_name="perfcalc",
)
