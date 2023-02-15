#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2023 Heinlein Consulting GmbH
#          Robert Sander <r.sander@heinlein-support.de>

#
# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.


from cmk.gui.i18n import _

from cmk.gui.plugins.metrics import (
    check_metrics,
    metric_info,
    graph_info,
)

metric_info['clients_registered'] = {
    'title' : _('Registered Clients'),
    'unit'  : 'count',
    'color' : '31/a',
}

metric_info['clients_active'] = {
    'title' : _('Active Clients'),
    'unit'  : 'count',
    'color' : '31/b',
}

metric_info['calls_active'] = {
    'title' : _('Active Calls'),
    'unit'  : 'count',
    'color' : '41/a',
}

metric_info['streams_active'] = {
    'title' : _('Active Streams'),
    'unit'  : 'count',
    'color' : '21/b',
}
