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
Check_MK perfometer definitions for USP SES

Authors:    Roger Ellenberger <roger.ellenberger@wagner.ch>

"""

from cmk.graphing.v1.perfometers import (
    FocusRange,
    Open,
    Closed,
    Perfometer,
    Stacked,
)

perfometer_usp_ses = Stacked(
    name="usp_ses",
    lower=Perfometer(
        name="lower",
        focus_range=FocusRange(
            lower=Closed(0),
            upper=Open(40000),
        ),
        segments=["avg_request_time"],
    ),
    upper=Perfometer(
        name="upper",
        focus_range=FocusRange(
            lower=Closed(0),
            upper=Open(90),
        ),
        segments=["requests_per_second"],
    )
)
