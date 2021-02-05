#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2014 Heinlein Support GmbH
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
    check_levels,
    check_levels_predictive,
    get_rate,
    get_value_store,
    register,
    render,
    Metric,
    Result,
    State,
    Service,
    )

from .utils import memory

import json
import time
import hashlib

ox_attributes = {
    'com.openexchange.pooling:name=Overview,NumConnections': 'DB Connections',
    'com.openexchange.monitoring:name=GeneralMonitor,NumberOfOpenAJPSockets': 'Open AJP Sockets',
    'com.openexchange.monitoring:name=GeneralMonitor,NumberOfIMAPConnections': 'IMAP Connections',
    'java.lang:type=OperatingSystem,OpenFileDescriptorCount': 'Open Files',
    'com.openexchange.monitoring:name=GeneralMonitor,NumberOfActiveSessions': 'Active Sessions',
    'com.openexchange.monitoring:name=GeneralMonitor,NumberOfAJAXConnections': 'AJAX Connections',
    'com.openexchange.monitoring:name=GeneralMonitor,NumberOfIdleMailConnections': 'Idle Mail Connections',
    'com.openexchange.monitoring:name=GeneralMonitor,NumberOfWebDAVUserConnections': 'WebDAV User Connections',
    'com.openexchange.monitoring:name=GeneralMonitor,NumberOfOutlookConnections': 'Outlook Connections',
    'com.openexchange.monitoring:name=GeneralMonitor,NumberOfSyncMLConnections': 'SyncML Connections',
    'com.openexchange.monitoring:name=MailInterfaceMonitor,NumActive': 'Mail Active Connections',
    'com.openexchange.monitoring:name=MailInterfaceMonitor,NumTimeoutConnections': 'Mail Timeout Connections',
    'com.openexchange.monitoring:name=MailInterfaceMonitor,NumSuccessfulLogins': 'Mail Successful Logins',
    'com.openexchange.monitoring:name=MailInterfaceMonitor,NumFailedLogins': 'Mail Failed Logins',
    'com.openexchange.monitoring:name=MailInterfaceMonitor,NumBrokenConnections': 'Mail Broken Connections',
    'com.openexchange.pooling:name=Overview,MasterConnectionsFetched': 'Master Connections',
    'com.openexchange.pooling:name=Overview,SlaveConnectionsFetched': 'Slave Connections',
    'com.openexchange.pooling:name=Overview,MasterInsteadOfSlave': 'Fallback Connections',
    'java.lang:type=Threading,ThreadCount': 'Thread Count',
    'com.openexchange.threadpool:name=ThreadPoolInformation,ActiveCount': 'Threadpool Active Threads Created',
    'com.openexchange.threadpool:name=ThreadPoolInformation,TaskCount': 'Threadpool Tasks Submitted',
    'com.openexchange.threadpool:name=ThreadPoolInformation,CompletedTaskCount': 'Threadpool Tasks Completed',
}

ox_counters = [
    'Mail Broken Connections',
    'Mail Successful Logins',
    'Mail Failed Logins',
    'ConfigDB Broken Read Connections',
    'ConfigDB Broken Write Connections',
    'Master Connections',
    'Slave Connections',
    'Fallback Connections',
    'Threadpool Tasks Submitted',
    'Threadpool Tasks Completed',
    ]

ox_sessions = {
    'com.openexchange.sessiond:name=SessionD Toolkit,NumberOfLongTermSessions': 'Long Term Sessions',
    'com.openexchange.sessiond:name=SessionD Toolkit,NumberOfShortTermSessions': 'Short Term Sessions',
}

def parse_ox_runtimestats(string_table):
    section = {'attr': {}, 'sessions': {}, 'memorypools': {}}

    ox_attr_keys = ox_attributes.keys()
    ox_session_keys = ox_sessions.keys()
    
    for line in string_table:
        try:
            name, value = line[0].split(' = ')
        except:
            continue
        if name in ox_attr_keys:
            section['attr'][ox_attributes[name]] = int(value)
        if name in ox_session_keys:
            section['sessions'][ox_sessions[name]] = json.loads(value)[0]
        if name.startswith('java.lang:') and name.endswith('type=MemoryPool,Usage'):
            poolname = None
            for key, val in map(lambda x: x.split('='), name[10:].split(',')):
                if key == 'name':
                    poolname = val
                    break
            if poolname:
                pool = {}
                if value[0] == '[' and value[-1] == ']':
                    for key, val in map(lambda x: x.split('='), value[1:-1].split(',')):
                        pool[key] = float(val)
                    if pool.get('max', 0) > 0:
                        section['memorypools'][poolname] = pool
    return section

register.agent_section(
    name="ox_runtimestats",
    parse_function=parse_ox_runtimestats,
)

def discover_ox_attributes(section) -> DiscoveryResult:
    for ox_attribute in section['attr'].keys():
        yield Service(item=ox_attribute)

def _per_second(item, value):
    return "%0.3f %s per second" % (value, item)

def _ox_label(item, value):
    return "%d %s" % (value, item)

def _check_value(item, value, levels, render_f):
    yield from check_levels_predictive(
        value,
        levels=levels,
        metric_name=item.replace(' ', '_'),
        render_func=render_f) if isinstance(levels, dict) else check_levels(
            value,
            levels_upper=levels,
            metric_name=item.replace(' ', '_'),
            render_func=render_f)

    # if not levels:
    #     yield Result(state=State.OK,
    #                  summary=render_f(value))
    #     yield Metric(item.replace(' ', '_'), value)
        
def check_ox_attributes(item, params, section) -> CheckResult:
    if item in section['attr']:
        levels = params.get('levels')
        if item in ox_counters:
            rate_per_sec = get_rate(get_value_store(),
                                    "ox_runtimestat.attributes.%s" % item,
                                    time.time(),
                                    section['attr'][item])
            yield from _check_value(item, rate_per_sec, levels, lambda x: _per_second(item, x))
        else:
            yield from _check_value(item, section['attr'][item], levels, lambda x: _ox_label(item, x))

register.check_plugin(
    name="ox_runtimestats_attributes",
    service_name="OX %s",
    sections=["ox_runtimestats"],
    discovery_function=discover_ox_attributes,
    check_function=check_ox_attributes,
    check_ruleset_name="open_xchange",
    check_default_parameters={},
)

def discover_ox_sessions(section) -> DiscoveryResult:
    for ox_session in section['sessions'].keys():
        yield Service(item=ox_session)

def check_ox_sessions(item, params, section) -> CheckResult:
    if item in section['sessions']:
        number = section['sessions'][item]
        yield Result(state=State.OK,
                     summary="%d %s" % (number, item))
        yield Metric(item.replace(' ', '_'), number)

register.check_plugin(
    name="ox_runtimestats_sessions",
    service_name="OX %s",
    sections=["ox_runtimestats"],
    discovery_function=discover_ox_sessions,
    check_function=check_ox_sessions,
    check_ruleset_name="open_xchange",
    check_default_parameters={},
)

def discover_ox_memorypool(section) -> DiscoveryResult:
    for ox_memorypool in section['memorypools'].keys():
        yield Service(item=ox_memorypool)

def check_ox_memorypool(item, params, section) -> CheckResult:
    if item in section['memorypools']:
        pool = section['memorypools'][item]
        warn, crit = params.get("levels", (None, None))
        mode = "abs_used" if isinstance(warn, int) else "perc_used"
        yield from memory.check_element(label='Usage',
                                        used=pool['used'],
                                        total=pool['max'],
                                        metric_name="mem_used",
                                        create_percent_metric=True,
                                        levels=(mode, (warn, crit)))

register.check_plugin(
    name="ox_runtimestats_memorypool",
    service_name="OX MemoryPool %s",
    sections=["ox_runtimestats"],
    discovery_function=discover_ox_memorypool,
    check_function=check_ox_memorypool,
    check_ruleset_name="memory_multiitem",
    check_default_parameters={},
)
