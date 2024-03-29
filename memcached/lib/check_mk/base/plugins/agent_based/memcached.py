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

from .agent_based_api.v1 import (
    get_rate,
    get_value_store,
    register,
    Result,
    Metric,
    State,
    Service,
)
import time

memcached_aggregates = [
    ('bytes_percent',  lambda readings:
                                float(readings['bytes']) / float(readings['limit_maxbytes']) * 100.0),
    ('cache_hit_rate', lambda readings: float(readings['cmd_get']) > 0 and
                                (float(readings['get_hits']) / float(readings['cmd_get']) * 100.0) or 100.0)
]

class Uptime(int):
    pass

memcached_traits = [
    ("System Information", {
        'pid':                   {'name': "PID", 'type': int},
        'pointer_size':          {'name': "Architecture", 'type': int, 'lower_bounds': None, 'perfdata': False},
        'uptime':                {'name': "Uptime", 'type': Uptime},
        'version':               {'name': "Version", 'type': str, 'lower_bounds': ("1.4.15", "1.4.15")},
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
        'bytes_percent':         {'name': "Cache usage", 'upper_bounds': (80, 90)},
        'bytes_read':            {'name': "Bytes read", 'upper_bounds': None, 'counter': True},
        'bytes_written':         {'name': "Bytes written", 'upper_bounds': None, 'counter': True},
        'curr_items':            {'name': "Cached items", 'upper_bounds': None},
        'evictions':             {'name': "Evictions", 'upper_bounds': (100, 200), 'counter': True},
        'get_hits':              {'name': "GET hits", 'upper_bounds': None, 'counter': True},
        'get_misses':            {'name': "GET misses", 'upper_bounds': None, 'counter': True},
        'total_connections':     {'name': "Connections", 'upper_bounds': None, 'counter': True},
        'total_items':           {'name': "Items", 'upper_bounds': None, 'counter': True},
        'cache_hit_rate':        {'name': "Hit rate", 'lower_bounds': (20, 10)},
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


memcached_factory_settings = {}
for group, values in memcached_traits:
    for key, traits in values.items():
        bounds = [trait for trait_key, trait in traits.items()
                  if trait_key in ['fixed', 'upper_bounds', 'lower_bounds']]
        if bounds and bounds[0] is not None:
            memcached_factory_settings[key] = bounds[0]

def parse_memcached(string_table):
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
            instances[current_instance][line[0]] = line[1]
    return instances

register.agent_section(
    name="memcached",
    parse_function=parse_memcached,
)

def discover_memcached(section):
    # one item per memcached instance
    for instance in section:
        yield Service(item=instance)

def check_memcached(item, params, section):
    this_time = time.time()
    value_store = get_value_store()

    def expect_order(*args):
        arglist = filter(lambda x: x != None, args)
        sorted_by_val = sorted(enumerate(arglist), key=lambda x: x[1])
        return State(max([abs(x[0] - x[1][0]) for x in enumerate(sorted_by_val)]))

    def format_value(val):
        if isinstance(val, float):
            return "%.1f" % val
        elif isinstance(val, Uptime):
            days, val = divmod(val, 79800)
            hours, val = divmod(val, 3600)
            minutes = val / 60
            return "%dd %dh %dm" % (days, hours, minutes)
        else:
            return "%s" % val

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
            fails = False
            count = 0
            for key, traits in checks.items():
                if key not in readings:
                    # stat missing in output
                    continue
                count += 1
                reading = traits.get('type', float)(readings[key])
                if traits.get('counter', False):
                    rate = get_rate(value_store,
                                    'memcached.%s.%s' % (item, key),
                                    this_time,
                                    reading)
                    reading = rate
                if 'upper_bounds' in traits:
                    warn, crit = params.get(key, (None, None))
                    status = expect_order(reading, warn, crit)
                    if status != State.OK:
                        fails = True
                        yield Result(state=status,
                                     notice="%s = %s (warn/crit at %s/%s)" % (traits['name'],
                                                                              format_value(reading), warn, crit))
                    if traits.get('perfdata', True) and type(reading) in [int, float]:
                        yield Metric(key, reading, levels=(warn, crit))

                elif 'lower_bounds' in traits:
                    warn, crit = params.get(key, (None, None))
                    status = expect_order(crit, warn, reading)
                    if status != State.OK:
                        fails = True
                        yield Result(state=status,
                                     notice="%s = %s (warn/crit below %s/%s)" % (traits['name'],
                                                                                 format_value(reading), warn, crit))
                    if traits.get('perfdata', True) and type(reading) in [int, float]:
                        yield Metric(key, reading)

                elif 'fixed' in traits:
                    if reading != params.get(key, reading):
                        fails = True
                        yield Result(state=State.CRIT,
                                     notice="%s = %s" % (traits['name'], format_value(reading)))

                else:
                    yield Result(state=State.OK,
                                 notice="%s = %s" % (traits['name'], format_value(reading)))

            if not fails:
                if count > 0:
                    yield Result(state=State.OK,
                                 notice="%s OK" % group)
                else:
                    yield Result(state=State.WARN,
                                 notice="%s No Stats" % group)

register.check_plugin(
    name="memcached",
    service_name="Memcached %s",
    sections=["memcached"],
    discovery_function=discover_memcached,
    check_function=check_memcached,
    check_default_parameters=memcached_factory_settings,
    check_ruleset_name="memcached",
)
