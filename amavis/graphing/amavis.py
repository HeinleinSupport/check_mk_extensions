#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2016 Heinlein Support GmbH
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

UNIT_COUNTER = metrics.Unit(metrics.DecimalNotation(''), metrics.StrictPrecision(2))
UNIT_PERCENTAGE = metrics.Unit(metrics.DecimalNotation('%'))
UNIT_PER_SECOND = metrics.Unit(metrics.DecimalNotation('/s'))

metric_amavis_ContentCleanMsgs = metrics.Metric(
    name='amavis_ContentCleanMsgs',
    title=Title("Amavis Clean Messages"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.LIGHT_GREEN,
)
metric_amavis_ContentCleanMsgs_percentage = metrics.Metric(
    name='amavis_ContentCleanMsgs_percentage',
    title=Title("Amavis Clean Messages %"),
    unit=UNIT_PERCENTAGE,
    color=metrics.Color.LIGHT_GREEN,
)
metric_amavis_ContentSpamMsgs = metrics.Metric(
    name='amavis_ContentSpamMsgs',
    title=Title("Amavis Spam Messages"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.ORANGE,
)
metric_amavis_ContentSpamMsgs_percentage = metrics.Metric(
    name='amavis_ContentSpamMsgs_percentage',
    title=Title("Amavis Spam Messages %"),
    unit=UNIT_PERCENTAGE,
    color=metrics.Color.ORANGE,
)
metric_amavis_ContentVirusMsgs = metrics.Metric(
    name='amavis_ContentVirusMsgs',
    title=Title("Amavis Virus Messages"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.RED,
)
metric_amavis_ContentVirusMsgs_percentage = metrics.Metric(
    name='amavis_ContentVirusMsgs_percentage',
    title=Title("Amavis Virus Messages %"),
    unit=UNIT_PERCENTAGE,
    color=metrics.Color.RED,
)
metric_amavis_InMsgs = metrics.Metric(
    name='amavis_InMsgs',
    title=Title("Amavis In Messages"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.LIGHT_GREEN,
)
metric_amavis_InMsgsStatusRejectedOriginating = metrics.Metric(
    name='amavis_InMsgsStatusRejectedOriginating',
    title=Title("Amavis Rejected Originating In Messages"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.ORANGE,
)
metric_amavis_InMsgsStatusRejectedOriginating_percentage = metrics.Metric(
    name='amavis_InMsgsStatusRejectedOriginating_percentage',
    title=Title("Amavis Rejected Originating In Messages %"),
    unit=UNIT_PERCENTAGE,
    color=metrics.Color.ORANGE,
)
metric_amavis_OutMsgs = metrics.Metric(
    name='amavis_OutMsgs',
    title=Title("Amavis Out Messages"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.LIGHT_GREEN,
)
metric_amavis_OutMsgsAttemptFails = metrics.Metric(
    name='amavis_OutMsgsAttemptFails',
    title=Title("Amavis Failed Out Attempts"),
    unit=UNIT_PER_SECOND,
    color=metrics.Color.YELLOW,
)
metric_amavis_child_avail = metrics.Metric(
    name='amavis_child_avail',
    title=Title("Amavis Available Child Processes"),
    unit=UNIT_COUNTER,
    color=metrics.Color.LIGHT_GREEN,
)
metric_amavis_child_busy = metrics.Metric(
    name='amavis_child_busy',
    title=Title("Amavis Busy Child Processes"),
    unit=UNIT_PERCENTAGE,
    color=metrics.Color.ORANGE,
)
