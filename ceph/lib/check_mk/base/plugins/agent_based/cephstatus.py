#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2017 Heinlein Support GmbH
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
    HostLabelGenerator,
)

from .agent_based_api.v1 import (
    get_value_store,
    register,
    render,
    HostLabel,
    Metric,
    Result,
    State,
    Service,
    )

from .utils import df

import json
import time
import re

def parse_cephstatus(string_table):
    section = {}
    for line in string_table:
        try:
            section.update(json.loads("".join([item for item in line])))
        except ValueError:
            pass
    return section

def host_label_cephstatus(section) -> HostLabelGenerator:
    if 'health' in section:
        yield HostLabel('ceph/mon', 'yes')
    
register.agent_section(
    name="cephstatus",
    parse_function=parse_cephstatus,
    host_label_function=host_label_cephstatus,
)

def discovery_cephstatus(section) -> DiscoveryResult:
    if 'health' in section:
        yield Service(item='Status')

def check_cephstatus(item, params, section) -> CheckResult:
    _single_state = { 'state': State.OK, 'count': 0 }
    _pgstates_list = ['activating+undersized',
                      'activating+undersized+degraded',
                      'active+clean',
                      'active+clean+inconsistent',
                      'active+clean+remapped',
                      'active+clean+scrubbing',
                      'active+clean+scrubbing+deep',
                      'active+clean+scrubbing+deep+repair',
                      'active+clean+scrubbing+deep+snaptrim_wait',
                      'active+clean+snaptrim',
                      'active+clean+snaptrim_wait',
                      'active+clean+wait',
                      'active+degraded',
                      'active+recovering',
                      'active+recovering+degraded',
                      'active+recovering+degraded+inconsistent',
                      'active+recovering+degraded+remapped',
                      'active+recovering+remapped',
                      'active+recovering+undersized',
                      'active+recovering+undersized+degraded+remapped',
                      'active+recovering+undersized+remapped',
                      'active+recovery_wait',
                      'active+recovery_wait+degraded',
                      'active+recovery_wait+degraded+inconsistent',
                      'active+recovery_wait+degraded+remapped',
                      'active+recovery_wait+remapped',
                      'active+recovery_wait+undersized+degraded',
                      'active+recovery_wait+undersized+degraded+remapped',
                      'active+recovery_wait+undersized+remapped',
                      'active+remapped',
                      'active+remapped+backfill_toofull',
                      'active+remapped+backfill_wait',
                      'active+remapped+backfill_wait+backfill_toofull',
                      'active+remapped+backfilling',
                      'active+remapped+inconsistent+backfilling',
                      'active+remapped+inconsistent+backfill_wait',
                      'active+undersized',
                      'active+undersized+degraded',
                      'active+undersized+degraded+inconsistent',
                      'active+undersized+degraded+remapped+backfilling',
                      'active+undersized+degraded+remapped+backfill_wait',
                      'active+undersized+degraded+remapped+inconsistent+backfilling',
                      'active+undersized+degraded+remapped+inconsistent+backfill_wait',
                      'active+undersized+remapped',
                      'active+undersized+remapped+backfill_wait',
                      'down',
                      'incomplete',
                      'peering',
                      'remapped+peering',
                      'stale+active+clean',
                      'stale+active+undersized',
                      'stale+active+undersized+degraded',
                      'stale+undersized+degraded+peered',
                      'stale+undersized+peered',
                      'undersized+degraded+peered',
                      'undersized+peered',
                      'unknown',
                     ]
    _ceph_pgstates = {}
    for state in _pgstates_list:
        _ceph_pgstates[state] = _single_state.copy()
    value_store = get_value_store()

    if 'health' in section:
        if 'status' in section['health']:
            if section['health']['status'] == 'HEALTH_OK':
                yield Result(state=State.OK,
                             summary='Overall Health OK')
            elif 'checks' in section['health']:
                for check, data in section['health']['checks'].items():
                    summary = check + ": " + data['summary']['message']
                    if data.get('muted', False):
                        state = State.OK
                        summary += " (muted)"
                    elif data['severity'] == 'HEALTH_WARN':
                        state = State.WARN
                    else:
                        state = State.CRIT
                    yield Result(state=state, summary=summary)
        elif 'overall_status' in section['health']:
            if section['health']['overall_status'] == 'HEALTH_OK':
                yield Result(state=State.OK,
                             summary='Overall Health OK')
            elif 'summary' in section['health']:
                for data in section['health']['summary']:
                    if data['severity'] == 'HEALTH_WARN':
                        yield Result(state=State.WARN,
                                     summary=data['summary'])
                    else:
                        yield Result(state=State.CRIT,
                                     summary=data['summary'])
        else:
            yield Result(state=State.UNKNOWN,
                         summary="Overall Health status not found: %s" % section['health'])
    else:
        yield Result(state=State.UNKNOWN,
                     summary="Overall Health not found")
    if 'osdmap' in section:
        if 'osdmap' in section['osdmap']:
            if 'full' in section['osdmap']['osdmap']:
                if section['osdmap']['osdmap']['full']:
                    yield Result(state=State.CRIT,
                                 summary='OSD Map full')
            if 'nearfull' in section['osdmap']['osdmap']:
                if section['osdmap']['osdmap']['nearfull']:
                    yield Result(state=State.WARN,
                                 summary='OSD Map near full')
    if 'pgmap' in section:
        pgmap = section['pgmap']
        if 'bytes_avail' in pgmap and 'bytes_total' in pgmap:
            size_mb = pgmap['bytes_total'] / 1048576.0
            avail_mb = pgmap['bytes_avail'] / 1048576.0
            yield from df.df_check_filesystem_single(value_store,
                                                     item,
                                                     size_mb,
                                                     avail_mb,
                                                     0,
                                                     None,
                                                     None,
                                                     params=params)
        if 'num_objects' in pgmap:
            yield Result(state=State.OK,
                         summary='%d Objects' % pgmap['num_objects'])
            yield Metric('num_objects', pgmap['num_objects'])
        if 'num_pgs' in pgmap:
            yield Result(state=State.OK,
                         summary='%d Placement Groups' % pgmap['num_pgs'])
            yield Metric('num_pgs', pgmap['num_pgs'])
        if 'degraded_objects' in pgmap and 'degraded_total' in pgmap and 'degraded_ratio' in pgmap:
            yield Metric('degraded_objects',
                         pgmap['degraded_objects'],
                         boundaries=(0, pgmap['degraded_total']))
        if 'misplaced_objects' in pgmap and 'misplaced_total' in pgmap and 'misplaced_ratio' in pgmap:
            yield Metric('misplaced_objects',
                         pgmap['misplaced_objects'],
                         boundaries=(0, pgmap['misplaced_total']))
        if 'recovering_bytes_per_sec' in pgmap:
            yield Result(state=State.OK,
                         summary='%s/s recovering' % render.bytes(pgmap['recovering_bytes_per_sec']))
            yield Metric('recovering', pgmap['recovering_bytes_per_sec'])
        if 'pgs_by_state' in pgmap:
            for pgstate in pgmap['pgs_by_state']:
                if pgstate['state_name'] in _ceph_pgstates:
                    _ceph_pgstates[pgstate['state_name']]['count'] = pgstate['count']
                else:
                    yield Result(state=State.UNKNOWN,
                                 summary='new PG state: ' + pgstate['state_name'])
                    continue
                if 'inconsistent' in pgstate['state_name'] or 'incomplete' in pgstate['state_name'] or 'active' not in pgstate['state_name']:
                    _ceph_pgstates[pgstate['state_name']]['state'] = State.CRIT
                elif 'active+clean' not in pgstate['state_name']:
                    _ceph_pgstates[pgstate['state_name']]['state'] = State.WARN
                if 'stale' in pgstate['state_name']:
                    _ceph_pgstates[pgstate['state_name']]['state'] = State.UNKNOWN
            for pgstate, info in _ceph_pgstates.items():
                if info['count'] > 0:
                    yield Result(state=info['state'],
                                 summary='%d PGs in %s' % (info['count'], pgstate))
                    yield Metric('pgstate_%s' % pgstate.replace('+', '_'), info['count'])
    if 'mgrmap' in section:
        if 'services' in section['mgrmap']:
            if 'dashboard' in section['mgrmap']['services']:
                yield Result(state=State.OK,
                             summary='Dashboard: %s' % section['mgrmap']['services']['dashboard'])

def cluster_check_cephstatus(item, params, section) -> CheckResult:
    # always take data from first node
    yield from check_cephstatus(item, params, section[list(section.keys())[0]])


register.check_plugin(
    name="cephstatus",
    service_name="Ceph %s",
    sections=["cephstatus"],
    discovery_function=discovery_cephstatus,
    check_function=check_cephstatus,
    check_ruleset_name="filesystem",
    check_default_parameters=df.FILESYSTEM_DEFAULT_PARAMS,
    cluster_check_function=cluster_check_cephstatus,
)
