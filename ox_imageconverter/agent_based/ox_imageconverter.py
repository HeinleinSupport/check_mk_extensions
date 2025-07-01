#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2023 Heinlein Support GmbH
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

from cmk.utils import debug
from pprint import pprint

def _render_requests(v):
    return "%0.3f requests/s" % v

_cache_attrs = {
    'CacheHitRatio': { 'desc': 'Cache Hit Ratio', 'metric': 'cache_hit_ratio', 'render': render.percent, 'factor': 100},
    'CacheKeyCount': { 'desc': 'Cache Key Count', 'metric': 'cache_key_count' },
    'CacheSize': { 'desc': 'Cache Size', 'metric': 'cache_size', 'render': render.bytes },
    'RequestCount_CacheAndGet': { 'desc': 'Requests for non-cached images', 'metric': 'requests_noncached_images', 'counter': True, 'render': _render_requests },
    'RequestCount_Get': { 'desc': 'Requests for cached images', 'metric': 'requests_cached_images', 'counter': True, 'render': _render_requests },
    'RequestCount_Total': { 'desc': 'Request Count Total', 'metric': 'requests_per_sec', 'counter': True, 'render': _render_requests },
    'MedianKeyProcessTimeMillis': { 'desc': 'Median Key Process Time', 'metric': 'average_processing_time', 'render': render.timespan, 'factor': 0.001 },
    'PeakKeyCountInQueue_Background': { 'desc': 'Peak Key Count Background', 'metric': 'peak_key_count_background' },
    'PeakKeyCountInQueue_Instant': { 'desc': 'Peak Key Count Instant', 'metric': 'peak_key_count_instant' },
    'PeakKeyCountInQueue_Medium': { 'desc': 'Peak Key Count Medium', 'metric': 'peak_key_count_medium' },
}

def parse_ox_imageconverter(string_table):
    section = {}

    data = json.loads(string_table[0][0])

    if data.get('api') == '1' and data.get('name') == 'imageconverter':
        section = data.get('metrics', {})
        section['status'] = data.get('status')

    if debug.enabled():
        pprint(section)
    return section

register.agent_section(
    name="ox_imageconverter",
    parse_function=parse_ox_imageconverter,
)

def discover_ox_imageconverter_cache(section) -> DiscoveryResult:
    if section.get('status') == 'running':
        yield Service()

def check_ox_imageconverter_cache(params, section) -> CheckResult:
    if debug.enabled():
        pprint(params)
    
    vs = get_value_store()
    now = time.time()
    for key in _cache_attrs.keys():
        data = section.get(key)
        attrs = _cache_attrs[key]
        if data != None:
            if attrs.get('counter'):
                value = get_rate(vs, 'ox_imageconverter_cache.%s' % key, now, data)
            else:
                value = data
            value *= attrs.get('factor', 1)
            if key in params:
                yield from check_levels(
                    value = value,
                    levels_upper = params[key].get('upper'),
                    levels_lower = params[key].get('lower'),
                    metric_name = attrs.get('metric'),
                    render_func = attrs.get('render', lambda x: str(x)),
                    label = attrs.get('desc'),
                    notice_only = True,
                )
            else:
                if attrs.get('metric'):
                    yield Metric(attrs.get('metric'), value)
                yield Result(state=State.OK,
                             notice='%s: %s' % (attrs['desc'], attrs.get('render', lambda x: str(x))(value)))

register.check_plugin(
    name="ox_imageconverter_cache",
    service_name="OX ImageConverter Cache",
    sections=["ox_imageconverter"],
    discovery_function=discover_ox_imageconverter_cache,
    check_function=check_ox_imageconverter_cache,
    check_ruleset_name="ox_imageconverter_cache",
    check_default_parameters={
        'CacheHitRatio': { 'lower': (60, 40) },
        'CacheKeyCount': { 'upper': (90000, 100000) },
        'CacheSize': { 'lower': (10737418240, 0), 'upper': (32212254720, 42949672960) },
        'MedianKeyProcessTimeMillis': { 'upper': (10, None) },
    },
)

