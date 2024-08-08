#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2017 Heinlein Support GmbH
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

from cmk.graphing.v1 import Title
from cmk.graphing.v1.metrics import (
    Color,
    DecimalNotation,
    IECNotation,
    Metric,
    StrictPrecision,
    Unit,
)

UNIT_METERS_PER_SECOND = Unit(IECNotation("m/s"))
UNIT_PERCENT = Unit(DecimalNotation("%"), StrictPrecision(2))

metric_chamber_perc = Metric(
    name = "chamber_perc",
    title = Title("Chamber Deviation"),
    unit = UNIT_PERCENT,
    color = Color.LIGHT_GREEN,
)

metric_airflow_meter = Metric(
    name = "airflow_meter",
    title = Title("Airflow"),
    unit = UNIT_METERS_PER_SECOND,
    color = Color.PURPLE,
)
