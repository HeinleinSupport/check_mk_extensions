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

# {u'pools': [{u'id': 1,
#             u'name': u'cephfs_data',
#             u'stats': {u'bytes_used': 0,
#                        u'dirty': 0,
#                        u'kb_used': 0,
#                        u'max_avail': 201491922944,
#                        u'objects': 0,
#                        u'percent_used': 0.0,
#                        u'quota_bytes': 0,
#                        u'quota_objects': 0,
#                        u'raw_bytes_used': 0,
#                        u'rd': 0,
#                        u'rd_bytes': 0,
#                        u'wr': 0,
#                        u'wr_bytes': 0}},

from .agent_based_api.v1.type_defs import (
    CheckResult,
    DiscoveryResult,
)

from .agent_based_api.v1 import (
    get_rate,
    get_value_store,
    register,
    render,
    Metric,
    Result,
    State,
    Service,
    )

from .utils import df

import json
import time

def parse_cephdf(string_table):
    section = {}
    for line in string_table:
        try:
            section.update(json.loads("".join([item for item in line])))
        except ValueError:
            pass
    return section

register.agent_section(
    name="cephdf",
    parse_function=parse_cephdf,
)

def discovery_cephdf(section) -> DiscoveryResult:
    for pool in section.get('pools', []):
        yield Service(item=pool['name'])

def check_cephdf(item, params, section) -> CheckResult:
    now = time.time()
    value_store = get_value_store()

    for pool in section.get('pools', []):
        if pool['name'] == item:
            stats = pool['stats']

            if stats['max_avail'] > 0:
                avail_mb = stats['max_avail'] / 1048576.0
                size_mb = avail_mb + stats['bytes_used'] / 1048576.0
            else:
                used_mb = stats['bytes_used'] / 1048576.0
                size_mb = used_mb / stats['percent_used']
                avail_mb = size_mb - used_mb

            yield from df.df_check_filesystem_single(value_store,
                                                     item,
                                                     size_mb,
                                                     avail_mb,
                                                     0,
                                                     None,
                                                     None,
                                                     params=params)
            yield Result(state=State.OK,
                         summary='%d Objects' % stats['objects'])
            yield Metric('num_objects', stats['objects'])

            rd_ios = get_rate(value_store, 'cephdf.%s.ri' % item, now, stats['rd'])
            rd_bytes = get_rate(value_store, 'cephdf.%s.rb' % item, now, stats['rd_bytes'])
            wr_ios = get_rate(value_store, 'cephdf.%s.wi' % item, now, stats['wr'])
            wr_bytes = get_rate(value_store, 'cephdf.%s.wb' % item, now, stats['wr_bytes'])

            yield Result(state=State.OK,
                         summary='IO: %0.2f Read IOPS, %0.2f Write IOPS, %s/s read, %s/s written' % (
                             rd_ios,
                             wr_ios,
                             render.bytes(rd_bytes),
                             render.bytes(wr_bytes)))
            yield Metric("disk_read_ios", rd_ios)
            yield Metric("disk_write_ios", wr_ios)
            yield Metric("disk_read_throughput", rd_bytes)
            yield Metric("disk_write_throughput", wr_bytes)

register.check_plugin(
    name="cephdf",
    service_name="Ceph Pool %s",
    sections=["cephdf"],
    discovery_function=discovery_cephdf,
    check_function=check_cephdf,
    check_ruleset_name="filesystem",
    check_default_parameters=df.FILESYSTEM_DEFAULT_LEVELS,
)
