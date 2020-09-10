#!/usr/bin/env python
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

from cmk.utils.render import physical_precision
from cmk.gui.plugins.metrics.check_mk import physical_precision_list

unit_info["m/s"] = {
    "title": _("Meters per second"),
    "symbol": _("m/s"),
    "render": lambda v: physical_precision(v, 3, _("m/s")),
    "graph_unit": lambda v: physical_precision_list(v, 3, _("m/s")),
}

metric_info["chamber_perc"] = {
    "title": _("Chamber Deviation"),
    "unit": "%",
    "color": "#88f060",
}

metric_info["airflow_meter"] = {
    "title": _("Airflow"),
    "unit": "m/s",
    "color": "#123456",
}
