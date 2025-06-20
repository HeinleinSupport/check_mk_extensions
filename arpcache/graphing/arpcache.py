#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2023 Heinlein Support GmbH
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

UNIT_NUMBER = metrics.Unit(metrics.DecimalNotation(''))

metric_ipneigh_delay = metrics.Metric(
    name='ipneigh_delay',
    title=Title("Neighbors Delay"),
    unit=UNIT_NUMBER,
    color=metrics.Color.YELLOW,
)
metric_ipneigh_failed = metrics.Metric(
    name='ipneigh_failed',
    title=Title("Neighbors Failed"),
    unit=UNIT_NUMBER,
    color=metrics.Color.YELLOW,
)
metric_ipneigh_incomplete = metrics.Metric(
    name='ipneigh_incomplete',
    title=Title("Neighbors Incomplete"),
    unit=UNIT_NUMBER,
    color=metrics.Color.YELLOW,
)
metric_ipneigh_noarp = metrics.Metric(
    name='ipneigh_noarp',
    title=Title("Neighbors noarp"),
    unit=UNIT_NUMBER,
    color=metrics.Color.DARK_PINK,
)
metric_ipneigh_none = metrics.Metric(
    name='ipneigh_none',
    title=Title("Neighbors None"),
    unit=UNIT_NUMBER,
    color=metrics.Color.YELLOW,
)
metric_ipneigh_permanent = metrics.Metric(
    name='ipneigh_permanent',
    title=Title("Neighbors Permanent"),
    unit=UNIT_NUMBER,
    color=metrics.Color.DARK_PINK,
)
metric_ipneigh_probe = metrics.Metric(
    name='ipneigh_probe',
    title=Title("Neighbors Probe"),
    unit=UNIT_NUMBER,
    color=metrics.Color.ORANGE,
)
metric_ipneigh_reachable = metrics.Metric(
    name='ipneigh_reachable',
    title=Title("Neighbors Reachable"),
    unit=UNIT_NUMBER,
    color=metrics.Color.ORANGE,
)
metric_ipneigh_stale = metrics.Metric(
    name='ipneigh_stale',
    title=Title("Neighbors Stale"),
    unit=UNIT_NUMBER,
    color=metrics.Color.YELLOW,
)
metric_ipneigh_total = metrics.Metric(
    name='ipneigh_total',
    title=Title("Neighbors Total"),
    unit=UNIT_NUMBER,
    color=metrics.Color.DARK_PURPLE,
)
