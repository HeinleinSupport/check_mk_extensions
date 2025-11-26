#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2025 Heinlein Support GmbH
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

metric_cartridges_used_black = metrics.Metric(name='cartridges_used_black', title=Title("Black Cartridges Used"), unit=UNIT_COUNTER, color=metrics.Color.BLACK,)
metric_cartridges_used_cyan = metrics.Metric(name='cartridges_used_cyan', title=Title("Cyan Cartridges Used"), unit=UNIT_COUNTER, color=metrics.Color.CYAN,)
metric_cartridges_used_magenta = metrics.Metric(name='cartridges_used_magenta', title=Title("Magenta Cartridges Used"), unit=UNIT_COUNTER, color=metrics.Color.DARK_PINK,)
metric_cartridges_used_other = metrics.Metric(name='cartridges_used_other', title=Title("Cartridges Used"), unit=UNIT_COUNTER, color=metrics.Color.DARK_BROWN,)
metric_cartridges_used_yellow = metrics.Metric(name='cartridges_used_yellow', title=Title("Yellow Cartridges Used"), unit=UNIT_COUNTER, color=metrics.Color.YELLOW,)
metric_pages_printed_black_white = metrics.Metric(name='pages_printed_black_white', title=Title("Black & White Pages Printed"), unit=UNIT_COUNTER, color=metrics.Color.DARK_GRAY,)
metric_pages_printed_economy = metrics.Metric(name='pages_printed_economy', title=Title("Economy Color Pages Printed"), unit=UNIT_COUNTER, color=metrics.Color.YELLOW,)
metric_pages_printed_full_color = metrics.Metric(name='pages_printed_full_color', title=Title("Full Color Pages Printed"), unit=UNIT_COUNTER, color=metrics.Color.DARK_PINK,)
metric_pages_printed_other = metrics.Metric(name='pages_printed_other', title=Title("Pages Printed"), unit=UNIT_COUNTER, color=metrics.Color.DARK_BROWN,)
metric_pages_printed_total = metrics.Metric(name='pages_printed_total', title=Title("Total Pages Printed"), unit=UNIT_COUNTER, color=metrics.Color.CYAN,)
