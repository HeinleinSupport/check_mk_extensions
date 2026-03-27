#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

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

"""
Check_MK metric definitions for USP SES

Authors:    Roger Ellenberger <roger.ellenberger@wagner.ch>

"""

from cmk.graphing.v1 import Title
from cmk.graphing.v1.metrics import (
    Color, 
    DecimalNotation,
    Metric,
    SINotation,
)


metric_avg_request_time = Metric(
    name="avg_request_time",
    title=Title("Average request time"),
    unit=SINotation(symbol="s"),
    color=Color.DARK_GRAY,
)

metric_active_users = Metric(
    name="active_users",
    title=Title("Active users"),
    unit=DecimalNotation("users"),
    color=Color.LIGHT_RED,
)

metric_client_connections = Metric(
    name="client_connections",
    title=Title("Client connections"),
    unit=DecimalNotation("connections"),
    color=Color.ORANGE,
)
