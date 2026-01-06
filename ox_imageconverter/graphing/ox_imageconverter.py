#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2023 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# tails. You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

from cmk.graphing.v1 import Title, graphs, metrics

UNIT_BYTES = metrics.Unit(metrics.IECNotation('B'))
UNIT_NUMBER = metrics.Unit(metrics.DecimalNotation(''))
REQUESTS_PER_SECOND = metrics.Unit(metrics.DecimalNotation('/s'))

metric_cache_key_count = metrics.Metric(
    name='cache_key_count',
    title=Title("Cache Key Count"),
    unit=UNIT_NUMBER,
    color=metrics.Color.PURPLE,
)
metric_cache_size = metrics.Metric(
    name='cache_size',
    title=Title("Cache Size"),
    unit=UNIT_BYTES,
    color=metrics.Color.DARK_PURPLE,
)
metric_peak_key_count_background = metrics.Metric(
    name='peak_key_count_background',
    title=Title("Peak Key Count Background"),
    unit=UNIT_NUMBER,
    color=metrics.Color.DARK_PINK,
)
metric_peak_key_count_instant = metrics.Metric(
    name='peak_key_count_instant',
    title=Title("Peak Key Count Instant"),
    unit=UNIT_NUMBER,
    color=metrics.Color.ORANGE,
)
metric_peak_key_count_medium = metrics.Metric(
    name='peak_key_count_medium',
    title=Title("Peak Key Count Medium"),
    unit=UNIT_NUMBER,
    color=metrics.Color.ORANGE,
)
metric_requests_cached_images = metrics.Metric(
    name='requests_cached_images',
    title=Title("Requests for cached Images"),
    unit=REQUESTS_PER_SECOND,
    color=metrics.Color.DARK_PINK,
)
metric_requests_noncached_images = metrics.Metric(
    name='requests_noncached_images',
    title=Title("Requests for non-cached Images"),
    unit=REQUESTS_PER_SECOND,
    color=metrics.Color.PINK,
)

graph_ox_imageconverter_cache_requests = graphs.Graph(
    name='ox_imageconverter_cache_requests',
    title=Title("Cache Requests"),
    simple_lines=[
        'requests_per_sec',
        'requests_noncached_images',
        'requests_cached_images',
    ],
)
