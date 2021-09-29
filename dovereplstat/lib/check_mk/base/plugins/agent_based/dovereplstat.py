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

# Output of doveadm replicator status

# Queued 'sync' requests        0                                                                          
# Queued 'high' requests        6766                                                                       
# Queued 'low' requests         2767                                                                       
# Queued 'failed' requests      20                                                                         
# Queued 'full resync' requests 2667                                                                       
# Waiting 'failed' requests     0                                                                          
# Total number of known users   38993
# Current users 3177

from .agent_based_api.v1.type_defs import (
    CheckResult,
    DiscoveryResult,
)

from .agent_based_api.v1 import (
    check_levels,
    register,
    render,
    Metric,
    Result,
    State,
    Service,
    )

def parse_dovereplstat(string_table):
    section={}
    for line in string_table:
        key = None
        val = None
        if line[1] in [ "'sync'", "'high'", "'low'", "'failed'" ]:
            key = line[1][1:-1] + '_requests'
            val = line[3]
        if line[1] == "'full":
            key = 'full_resync_requests'
            val = line[4]
        if line[:-1] == [u'Total', u'number', u'of', u'known', u'users']:
            key = 'total_users'
            val = line[5]
        if line[:-1] == [u'Current', u'users']:
            key = 'current_users'
            val = line[2]
        if key:
            try:
                section[key] = {'value': int(val), 'label': " ".join(line[:-1])}
            except ValueError:
                pass
    return section        

register.agent_section(
    name="dovereplstat",
    parse_function=parse_dovereplstat,
)

def discovery_dovereplstat(section) -> DiscoveryResult:
    if 'total_users' in section:
        yield Service()

def check_dovereplstat(params, section) -> CheckResult:
    perfdata = []
    msg = []
    rc = 0
    total_users = 0
    current_users = 0
    for key, data in section.items():
        if params and key in params:
            yield from check_levels(data['value'],
                                    levels_upper=params[key],
                                    metric_name=key,
                                    label=data['label'],
                                    notice_only=True)
        else:
            yield Result(state=State.OK,
                         notice="%s: %d" % (data['label'], data['value']))
            yield Metric(key, data['value'])
    if 'total_users' in section and section['total_users']['value'] != 0:
        perc_users = section.get('current_users', {'value': 0})['value'] * 100.0 / section['total_users']['value']
        yield Result(state=State.OK,
                     summary='%0.2f%% user usage' % perc_users)
        yield Metric('perc_users', perc_users)

register.check_plugin(
    name="dovereplstat",
    service_name="Dovecot Replicator Status",
    sections=["dovereplstat"],
    discovery_function=discovery_dovereplstat,
    check_function=check_dovereplstat,
    check_ruleset_name="dovereplstat",
    check_default_parameters={},
)

