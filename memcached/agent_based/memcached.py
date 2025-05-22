#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2020 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.


# <<<memcached>>>
# [localhost:11211]
#          accepting_conns           1
#                auth_cmds           0
#              auth_errors           0
#                    bytes           0
#               bytes_read          66
#    ...

import time
from collections.abc import Mapping # type: ignore
from typing import Any # type: ignore
from packaging.version import Version

from cmk.agent_based.v2 import (
    AgentSection,
    check_levels,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    get_rate,
    get_value_store,
    render,
    Result,
    Service,
    State,
    StringTable,
)

Section = Mapping[str, Any]

memcached_aggregates = [
    (
        'bytes_percent',
        lambda readings: readings['bytes'] / readings['limit_maxbytes'] * 100.0
    ),
    (
        'cache_hit_rate',
        lambda readings: readings['cmd_get'] > 0 and (readings['get_hits'] / readings['cmd_get'] * 100.0) or 100.0
    ),
]

class Uptime(int):
    pass

memcached_traits = [
    ("System Information", {
        'pid':                   {'name': "PID", 'type': int},
        'pointer_size':          {'name': "Architecture", 'type': int, 'lower_bounds': None, 'perfdata': False, "render": lambda x: f"{x} bits"},
        'uptime':                {'name': "Uptime", 'type': Uptime, "render": render.timespan},
        'version':               {'name': "Version", 'type': str},
#        'rusage_system':         {'name': "CPU usage system", 'upper_bounds': None},
#        'rusage_user':           {'name': "CPU usage user", 'upper_bounds': None},
        'threads':               {'name': "Threads", 'upper_bounds': None},
    }),
    ("Operational", {
        'accepting_conns':       {'name': "Accepting Connections", 'type': int, 'fixed': 1},
    }),
    ("Authentification", {
        'auth_cmds':             {'name': "Authentifications", 'upper_bounds': None, 'counter': True},
        'auth_errors':           {'name': "Failed Authentifications", 'upper_bounds': None, 'counter': True},
    }),
    ("Cache Data", {
        'bytes_percent':         {'name': "Cache usage", 'upper_bounds': (80, 90), "render": render.percent},
        'bytes_read':            {'name': "Bytes read", 'upper_bounds': None, 'counter': True, "render": render.iobandwidth},
        'bytes_written':         {'name': "Bytes written", 'upper_bounds': None, 'counter': True, "render": render.iobandwidth},
        'curr_items':            {'name': "Cached items", 'upper_bounds': None},
        'evictions':             {'name': "Evictions", 'upper_bounds': (100, 200), 'counter': True},
        'get_hits':              {'name': "GET hits", 'upper_bounds': None, 'counter': True},
        'get_misses':            {'name': "GET misses", 'upper_bounds': None, 'counter': True},
        'total_connections':     {'name': "Connections", 'upper_bounds': None, 'counter': True},
        'total_items':           {'name': "Items", 'upper_bounds': None, 'counter': True},
        'cache_hit_rate':        {'name': "Hit rate", 'lower_bounds': (20, 10), "render": render.percent},
    }),
    ("CAS Data", {
        'cas_badval':            {'name': "CAS bad value", 'upper_bounds': (5, 10), 'counter': True},
        'cas_hits':              {'name': "CAS hits", 'upper_bounds': None, 'counter': True},
        'cas_misses':            {'name': "CAS misses", 'upper_bounds': None, 'counter': True},
    }),
    ("Commands", {
        'cmd_flush':             {'name': "FLUSH commands", 'upper_bounds': (1, 5), 'counter': True},
        'cmd_get':               {'name': "GET commands", 'upper_bounds': None, 'counter': True},
        'cmd_set':               {'name': "SET commands", 'upper_bounds': None, 'counter': True},
    }),
    ("Connections", {
        'connection_structures': {'name': "Connection Structures", 'upper_bounds': None},
        'curr_connections':      {'name': "open connections", 'upper_bounds': None},
        'listen_disabled_num':   {'name': "Times listen disabled", 'upper_bounds': (5, 10), 'counter': True},
    }),
    ("Connection Overflow", {
        'conn_yields':           {'name': "Connection yields", 'upper_bounds': (1, 5), 'counter': True},
    }),
    ("Increase/Decrease", {
        'decr_hits':             {'name': "Decrease hits", 'upper_bounds': None, 'counter': True},
        'decr_misses':           {'name': "Decrease misses", 'upper_bounds': None, 'counter': True},
        'incr_hits':             {'name': "Increase hits", 'upper_bounds': None, 'counter': True},
        'incr_misses':           {'name': "Increase misses", 'upper_bounds': None, 'counter': True},
    }),
    ("Deletions", {
        'delete_hits':           {'name': "Delete hits", 'upper_bounds': None, 'counter': True},
        'delete_misses':         {'name': "Delete misses", 'upper_bounds': (1000, 2000), 'counter': True},
    }),
    ("Reclaim", {
        'reclaimed':             {'name': "Reclaimed", 'upper_bounds': None, 'counter': True}
    })
]

memcached_types = {
    'bytes': int,
    'limit_maxbytes': int,
}
memcached_factory_settings = {}
for group, values in memcached_traits:
    for key, traits in values.items():
        bounds = [trait for trait_key, trait in traits.items()
                  if trait_key in ['fixed', 'upper_bounds', 'lower_bounds']]
        if bounds and bounds[0] is not None:
            memcached_factory_settings[key] = ("fixed", bounds[0])
        memcached_types[key] = traits.get("type", int)
        if traits.get("counter") and not traits.get("render"):
            traits["render"] = lambda x: f"{x} /s"
        if not traits.get("render"):
            traits["render"] = lambda x: str(x)

def parse_memcached(string_table: StringTable) -> Section:
    instances = {}
    current_instance = None
    for line in string_table:
        if not line:
            continue
        if line[0].startswith("["):
            current_instance = line[0].strip("[]")
            instances[current_instance] = {}
        elif current_instance is None:
            raise Exception("expected instance name")
        else:
            if line[0] in memcached_types:
                instances[current_instance][line[0]] = memcached_types[line[0]](line[1])
    return instances

agent_section_memcached = AgentSection(
    name="memcached",
    parse_function=parse_memcached,
)

def discover_memcached(section: Section) -> DiscoveryResult:
    # one item per memcached instance
    for instance in section:
        yield Service(item=instance)

def check_version(value: str, params: None | Mapping[str, str]) -> CheckResult:
    version = Version(value)
    params = params or {}
    warn = Version(params.get("warn", "0"))
    crit = Version(params.get("crit", "0"))
    state = State.OK
    if version < crit:
        state = State.CRIT
    elif version < warn:
        state = State.WARN
    yield Result(
        state=state,
        notice=f"Version: {value}",
    )

def check_memcached(item: str, params: Mapping[str, Any], section: Section) -> CheckResult:
    this_time = time.time()
    value_store = get_value_store()

    if item in section:
        status = []
        readings = section[item]
        # calculate aggregates
        for aggregate, func in memcached_aggregates:
            try:
                readings[aggregate] = func(readings)
            except KeyError:
                # stat missing from output
                pass

        for group, checks in memcached_traits:
            count = 0
            for key, traits in checks.items():
                if key not in readings:
                    # stat missing in output
                    continue
                count += 1
                reading = readings[key]
                if traits.get('counter', False):
                    rate = get_rate(
                        value_store,
                        'memcached.%s.%s' % (item, key),
                        this_time,
                        reading
                    )
                    reading = rate
                if key == "version":
                    yield from check_version(
                        reading,
                        params.get(key),
                    )
                elif 'upper_bounds' in traits:
                    yield from check_levels(
                        value=reading,
                        levels_upper=params.get(key),
                        notice_only=True,
                        metric_name=traits.get('perfdata', True) and key or None,
                        render_func=traits.get("render"),
                        label=traits["name"],
                    )
                elif 'lower_bounds' in traits:
                    yield from check_levels(
                        value=reading,
                        levels_lower=params.get(key),
                        notice_only=True,
                        metric_name=traits.get('perfdata', True) and key or None,
                        render_func=traits.get("render"),
                        label=traits["name"],
                    )
                elif 'fixed' in traits:
                    p = params.get(key)
                    if p and reading != p[1]:
                        yield Result(state=State.CRIT,
                                    notice="%s = %s" % (traits['name'], traits.get("render")(reading)))
                else:
                    yield Result(state=State.OK,
                                 notice="%s = %s" % (traits['name'], traits.get("render")(reading)))
            if not count:
                yield Result(
                    state=State.WARN,
                    notice="%s No Stats" % group
                )

check_plugin_memcached = CheckPlugin(
    name="memcached",
    service_name="Memcached %s",
    sections=["memcached"],
    discovery_function=discover_memcached,
    check_function=check_memcached,
    check_default_parameters=memcached_factory_settings,
    check_ruleset_name="memcached",
)
