#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2020 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>
#

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2. This file is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

from cmk.graphing.v1 import Title, graphs, metrics

UNIT_BYTES_PER_SECOND = metrics.Unit(metrics.IECNotation('B/s'))
UNIT_NUMBER = metrics.Unit(metrics.DecimalNotation(''))
UNIT_PERCENTAGE = metrics.Unit(metrics.DecimalNotation('%'))
UNIT_PER_SECOND = metrics.Unit(metrics.DecimalNotation('/s'))

metric_auth_cmds = metrics.Metric(
    name='auth_cmds',
    title=Title("Authorizations"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.CYAN,)
metric_auth_errors = metrics.Metric(
    name='auth_errors',
    title=Title("Authorization Errors"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.DARK_PINK,)
metric_bytes_percent = metrics.Metric(
    name='bytes_percent',
    title=Title("Cache Usage"),
    unit=UNIT_PERCENTAGE,
    color=metrics.Color.CYAN,)
metric_bytes_read = metrics.Metric(
    name='bytes_read',
    title=Title("Read"),
    unit=UNIT_BYTES_PER_SECOND,
    color=metrics.Color.CYAN,)
metric_bytes_written = metrics.Metric(
    name='bytes_written',
    title=Title("Written"),
    unit=UNIT_BYTES_PER_SECOND,
    color=metrics.Color.BLUE,)
metric_cache_hit_rate = metrics.Metric(
    name='cache_hit_rate',
    title=Title("Rate of cache hits"),
    unit=UNIT_PERCENTAGE,
    color=metrics.Color.DARK_PURPLE,)
metric_cas_badval = metrics.Metric(
    name='cas_badval',
    title=Title("CAS bad identifier"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.DARK_PINK,)
metric_cas_hits = metrics.Metric(
    name='cas_hits',
    title=Title("CAS hits"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.CYAN,)
metric_cas_misses = metrics.Metric(
    name='cas_misses',
    title=Title("CAS misses"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.YELLOW,)
metric_cmd_flush = metrics.Metric(
    name='cmd_flush',
    title=Title("Flush Commands"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.DARK_BLUE,)
metric_cmd_get = metrics.Metric(
    name='cmd_get',
    title=Title("GET Commands"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.YELLOW,)
metric_cmd_set = metrics.Metric(
    name='cmd_set',
    title=Title("SET Commands"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.CYAN,)
metric_conn_yields = metrics.Metric(
    name='conn_yields',
    title=Title("Forced connection yields"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.ORANGE,)
metric_connection_structures = metrics.Metric(
    name='connection_structures',
    title=Title("Connection Structures"),
    unit=UNIT_NUMBER,
    color=metrics.Color.DARK_PURPLE,)
metric_curr_connections = metrics.Metric(
    name='curr_connections',
    title=Title("Current Connections"),
    unit=UNIT_NUMBER,
    color=metrics.Color.YELLOW,)
metric_curr_items = metrics.Metric(
    name='curr_items',
    title=Title("Items in cache"),
    unit=UNIT_NUMBER,
    color=metrics.Color.BLUE,)
metric_decr_hits = metrics.Metric(
    name='decr_hits',
    title=Title("Decrease Hits"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.DARK_PURPLE,)
metric_decr_misses = metrics.Metric(
    name='decr_misses',
    title=Title("Decrease misses"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.ORANGE,)
metric_delete_hits = metrics.Metric(
    name='delete_hits',
    title=Title("Delete Hits"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.DARK_BLUE,)
metric_delete_misses = metrics.Metric(
    name='delete_misses',
    title=Title("Delete misses"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.DARK_PINK,)
metric_evictions = metrics.Metric(
    name='evictions',
    title=Title("Evictions"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.YELLOW,)
metric_get_hits = metrics.Metric(
    name='get_hits',
    title=Title("GET Hits"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.CYAN,)
metric_get_misses = metrics.Metric(
    name='get_misses',
    title=Title("GET Misses"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.DARK_PINK,)
metric_incr_hits = metrics.Metric(
    name='incr_hits',
    title=Title("Increase Hits"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.DARK_BLUE,)
metric_incr_misses = metrics.Metric(
    name='incr_misses',
    title=Title("Increase misses"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.DARK_PINK,)
metric_listen_disabled_num = metrics.Metric(
    name='listen_disabled_num',
    title=Title("Listen disabled"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.ORANGE,)
metric_reclaimed = metrics.Metric(
    name='reclaimed',
    title=Title("Items reclaimed"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.YELLOW,)
metric_rusage_system = metrics.Metric(
    name='rusage_system',
    title=Title("System CPU time used"),
    unit=UNIT_NUMBER,
    color=metrics.Color.BLUE,)
metric_rusage_user = metrics.Metric(
    name='rusage_user',
    title=Title("User CPU time used"),
    unit=UNIT_NUMBER,
    color=metrics.Color.CYAN,)
# metric_threads = metrics.Metric(
#     name='threads',
#     title=Title("Threads"),
#     unit=UNIT_NUMBER,
#     color=metrics.Color.CYAN,)
metric_total_connections = metrics.Metric(
    name='total_connections',
    title=Title("Connections"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.CYAN,)
metric_total_items = metrics.Metric(
    name='total_items',
    title=Title("Items stored"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.CYAN,)

graph_memcached_authorizations = graphs.Graph(
    name='memcached_authorizations',
    title=Title("Authorizations"),
    compound_lines=['auth_cmds'],
    simple_lines=['auth_errors'],)
graph_memcached_cas = graphs.Graph(
    name='memcached_cas',
    title=Title("CAS"),
    compound_lines=['cas_hits',
    'cas_misses',],
    simple_lines=['cas_badval'],)
graph_memcached_commands = graphs.Graph(
    name='memcached_commands',
    title=Title("Commands"),
    compound_lines=['cmd_get',
    'cmd_set',
    'cmd_flush',],)
graph_memcached_cpu_usage = graphs.Graph(
    name='memcached_cpu_usage',
    title=Title("CPU usage"),
    compound_lines=['rusage_user',
    'rusage_system',],)
graph_memcached_deletions = graphs.Graph(
    name='memcached_deletions',
    title=Title("Deletions"),
    compound_lines=['delete_hits',
    'delete_misses',],)
graph_memcached_get = graphs.Graph(
    name='memcached_get',
    title=Title("GET"),
    compound_lines=['get_hits',
    'get_misses',],
    simple_lines=['cmd_get'],)
graph_memcached_incdec = graphs.Bidirectional(
    name='memcached_incdec',
    title=Title("Increase/Decrease"),
    lower=graphs.Graph(
        name='memcached_incdec_lower',
        title=Title("Increase/Decrease"),
        compound_lines=['decr_hits',
        'decr_misses',],),
    upper=graphs.Graph(
        name='memcached_incdec_upper',
        title=Title("Increase/Decrease"),
        compound_lines=['incr_hits',
        'incr_misses',],),)
graph_memcached_rw = graphs.Bidirectional(
    name='memcached_rw',
    title=Title("Read and written"),
    lower=graphs.Graph(
        name='memcached_rw_lower',
        title=Title("Read and written"),
        compound_lines=['bytes_written'],),
    upper=graphs.Graph(
        name='memcached_rw_upper',
        title=Title("Read and written"),
        compound_lines=['bytes_read'],),)

