#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2018 Heinlein Support GmbH
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

metric_info["freq_cpu_avg"] = {
    "title" : _("Average Frequency"),
    "unit"  : "hz",
    "color" : "#000000",
}

for i in range(MAX_CORES):
    metric_info['freq_cpu%d' % i] = {
        'title' : _('Frequency CPU %d') % i,
        'unit'  : 'hz',
        'color' : indexed_color(i, MAX_CORES)
}

graph_info["cpu_frequencies"] = {
    'title': _('CPU Freqencies'),
    'metrics': [ ( 'freq_cpu%d' % num, 'line' ) for num in range(MAX_CORES) ] + [ ( 'freq_cpu_avg', 'line' ) ],
    'optional_metrics' : [ 'freq_cpu%d' % num for num in range(MAX_CORES) ],
}
