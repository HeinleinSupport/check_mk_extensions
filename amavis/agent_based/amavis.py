#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2016 Heinlein Support GmbH
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

from collections.abc import Mapping # type: ignore
from typing import Any # type: ignore

from cmk.agent_based.v2 import (
    AgentSection,
    check_levels,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    get_rate,
    get_value_store,
    Metric,
    render,
    Result,
    Service,
    State,
    StringTable,
)

import time

Section = Mapping[str, Any]

def parse_amavis(string_table: StringTable) -> Section:
    parsed = {'ps': [], 'agent': {}}
    in_ps = False
    in_agent = False
    for line in string_table:
        if len(line) == 1:
            if line[0] == '[ps]':
                in_ps = True
                in_agent = False
                continue
            if line[0] == '[agent]':
                in_ps = False
                in_agent = True
                continue
        if in_ps:
            parsed['ps'].append((line[4], " ".join(line[5:])))
        if in_agent:
            parsed['agent'][line[0]] = line[1:]
    return parsed

agent_section_amavis = AgentSection(
    name="amavis",
    parse_function=parse_amavis,
)

def discovery_amavis(section: Section) -> DiscoveryResult:
    if section and section['ps']:
        yield Service()

def check_amavis(params, section: Section) -> CheckResult:
    if section['ps']:
        perfdata = []
        this_time = int(time.time())
        value_store = get_value_store()
        
        master_proc = 0
        child_procs = 0
        child_avail = 0
        for proc in section['ps']:
            if proc[1] == u'(master)':
                master_proc += 1
            if proc[1] == u'(virgin child)':
                child_procs += 1
                child_avail += 1
            if proc[1].startswith(u'(ch'):
                child_procs += 1
                if proc[1].endswith(u'-avail)'):
                    child_avail += 1
        if master_proc > 1:
            yield Result(state=State.CRIT,
                         summary='More than one amavisd master process running: %d' % master_proc)
        elif master_proc == 0:
            yield Result(state=State.CRIT,
                         summary='No amavisd master process running')
        else:
            yield Result(state=State.OK,
                         summary='Amavis master process running')
        yield Result(state=State.OK,
                     summary='%d child processes running' % child_procs)
        yield Result(state=State.OK,
                     summary='%d child processes available' % child_avail)

        yield Metric(
            'amavis_child_avail',
            child_avail,
            boundaries=(0, child_procs)
        )
        
        busy_childs_percentage = 0
        if child_procs > 0:
            busy_childs_percentage = ( child_procs - child_avail ) * 100.0 / child_procs
            
        yield from check_levels(
            value = busy_childs_percentage,
            levels_upper = params.get("busy_childs"),
            metric_name = "amavis_child_busy",
            label = "Busy Childs",
            render_func = render.percent,
            boundaries = (0.0, 100.0),
            notice_only = True,
        )

        metrics = [ 'ContentCleanMsgs',
                    'ContentSpamMsgs',
                    'ContentVirusMsgs',
                    'InMsgs',
                    'OutMsgs',
                    'OutMsgsAttemptFails',
                    'InMsgsStatusRejectedOriginating' ]
        percentage = { 'total': 0,
                       'parts': {'ContentCleanMsgs': 0,
                                 'ContentSpamMsgs': 0,
                                 'ContentVirusMsgs': 0,
                                 'InMsgsStatusRejectedOriginating': 0 } }
        for metric in metrics:
            if metric in section['agent']:
                rate = get_rate(value_store, 'amavis.%s' % metric, this_time, int(section['agent'][metric][0]))
                yield Metric('amavis_%s' % metric, rate)
                if metric == percentage['total']:
                    percentage['total'] = rate
                if metric in percentage['parts'].keys():
                    percentage['parts'][metric] = rate
        for part, value in percentage['parts'].items():
            if percentage['total'] > 0 and value > 0:
                yield Metric('amavis_%s_percentage' % part,
                             value * 100.0 / percentage['total'])
            else:
                yield Metric('amavis_%s_percentage' % part, 0.0)

check_plugin_amavis = CheckPlugin(
    name="amavis",
    service_name="Amavis",
    sections=["amavis"],
    discovery_function=discovery_amavis,
    check_function=check_amavis,
    check_default_parameters={
        'busy_childs': ("fixed", (75, 95)),
    },
    check_ruleset_name="amavis",
)
