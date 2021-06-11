#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2015 Heinlein Support GmbH
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
    check_levels_predictive,
    register,
    render,
    Metric,
    Result,
    Service,
    State,
)

def parse_otrs(string_table):
    otrs = {}
    for line in string_table:
        if line[0] not in otrs:
            otrs[line[0]] = {}
        otrs[line[0]][int(line[1])] = {'total': int(line[2]), 'state': " ".join(line[3:])}
    return otrs

register.agent_section(
    name="otrs",
    parse_function=parse_otrs,
)

def discover_otrs(section):
    for queue in section:
        yield Service(item=queue)

def _render_tickets(value):
    if value is None:
        return ''
    return "%d Tickets" % value

def check_otrs(item, params, section):
    paramstate = {}
    if 'levels' in params:
        for listofstates, levels in params['levels']:
            for state in listofstates:
                paramstate[state] = levels
    if item in section:
        for ticket_state, data in section[item].items():
            total = data['total']
            state = data['state']
            dsname = state.replace(' ', '_').replace(',', '_').replace('.', '_')
            if state in paramstate:
                if isinstance(paramstate[state], tuple):
                    yield from check_levels(
                        total,
                        levels_upper=paramstate[state],
                        metric_name=dsname,
                        label=state,
                        render_func=_render_tickets,
                        notice_only=True,
                    )
                elif isinstance(paramstate[state], dict):
                    yield from check_levels_predictive(
                        total,
                        levels=paramstate[state],
                        metric_name=dsname,
                        label=state,
                        render_func=_render_tickets,
                    )
                else:
                    yield Metric(dsname, total)
                    yield Result(state=State.OK,
                                 notice='%s: %s' % (state, _render_tickets(total)))
            else:
                yield Metric(dsname, total)
                yield Result(state=State.OK,
                             notice='%s: %s' % (state, _render_tickets(total)))

register.check_plugin(
    name="otrs",
    service_name="OTRS %s",
    sections=["otrs"],
    discovery_function=discover_otrs,
    check_function=check_otrs,
    check_default_parameters={
        'levels': [ (['new'], ( 50, 100 )) ],
    },
    check_ruleset_name="otrs",
)
