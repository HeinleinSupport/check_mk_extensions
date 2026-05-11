#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2026 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>
#

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

from cmk.graphing.v1 import Title, metrics

UNIT_COUNT = metrics.Unit(metrics.DecimalNotation(''), metrics.StrictPrecision(0))
UNIT_PER_SECOND = metrics.Unit(metrics.DecimalNotation('/s'))
UNIT_TIME = metrics.Unit(metrics.TimeNotation())

# xspct_db_metrics = {
#     "event_loop_lag_seconds": "Event Loop Lag",
#     "xspct_db_foreground_overloaded": "Foreground Overloaded",
#     "xspct_db_requests_timeout": "Requests Timeout",
#     "xspct_db_background_rejected": "Background Rejected",
#     "xspct_db_background_errors": "Background Errors",
#     "xspct_db_prefilter_domain_count": "Prefilter Domain Count",
#     "http_requests_in_flight": "HTTP Requests",
# }

# counter: xspct_db_background_errors
# counter: xspct_db_background_rejected
# gauge: event_loop_lag_seconds
# counter: xspct_db_foreground_overloaded
# gauge: http_requests_in_flight
# gauge: xspct_db_prefilter_domain_count
# counter: xspct_db_requests_timeout

metric_http_requests_in_flight = metrics.Metric(
    name="http_requests_in_flight",
    title=Title("HTTP Requests"),
    unit=UNIT_COUNT,
    color=metrics.Color.YELLOW,
)

metric_xspct_db_prefilter_domain_count = metrics.Metric(
    name="xspct_db_prefilter_domain_count",
    title=Title("Prefilter Domain Count"),
    unit=UNIT_COUNT,
    color=metrics.Color.GREEN,
)

metric_xspct_db_background_errors_total = metrics.Metric(
    name="xspct_db_background_errors_total",
    title=Title("Background Errors"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.RED,
)

metric_xspct_db_background_rejected_total = metrics.Metric(
    name="xspct_db_background_rejected_total",
    title=Title("Background Rejected"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.PURPLE,
)

metric_xspct_db_requests_timeout_total = metrics.Metric(
    name="xspct_db_requests_timeout_total",
    title=Title("Requests Timeout"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.BLUE,
)

metric_event_loop_lag_seconds = metrics.Metric(
    name="event_loop_lag_seconds",
    title=Title("Event Loop Lag"),
    unit=UNIT_TIME,
    color=metrics.Color.DARK_YELLOW,
)

metric_xspct_db_foreground_overloaded_total = metrics.Metric(
    name="xspct_db_foreground_overloaded_total",
    title=Title("Foreground Overloaded"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.GRAY,
)
