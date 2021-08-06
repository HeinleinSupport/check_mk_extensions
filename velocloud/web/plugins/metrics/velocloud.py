#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2020 Heinlein Support GmbH
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

metric_info['tx_jitter'] = {
    'title' : _('TX Jitter'),
    'unit'  : 's',
    'color' : '31/a',
}

metric_info['rx_jitter'] = {
    'title' : _('RX Jitter'),
    'unit'  : 's',
    'color' : '31/b',
}

metric_info['tx_latency'] = {
    'title' : _('TX Latency'),
    'unit'  : 's',
    'color' : '41/a',
}

metric_info['rx_latency'] = {
    'title' : _('RX Latency'),
    'unit'  : 's',
    'color' : '41/b',
}

graph_info['if_errors'] = {
    'title': _('Errors'),
    'metrics': [
        ('if_in_errors', 'line'),
        ('if_out_errors', '-line'),
    ],
}

graph_info['jitter'] = {
    'title': _('Jitter'),
    'metrics': [
        ('rx_jitter', 'line'),
        ('tx_jitter', '-line'),
    ],
}

graph_info['latency'] = {
    'title': _('Latency'),
    'metrics': [
        ('rx_latency', 'line'),
        ('tx_latency', '-line'),
    ],
}

graph_info['unicast_packets'] = {
    'title': _('Unicast Packets'),
    'metrics': [
        ('if_in_unicast', 'line'),
        ('if_out_unicast', '-line'),
    ],
}
