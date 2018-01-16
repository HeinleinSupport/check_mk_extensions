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

metric_info['num_objects'] = {
    'title' : _('Number of Objects'),
    'unit'  : 'count',
    'color' : '51/a',
}

metric_info['num_pgs'] = {
    'title' : _('Number of Placement Groups'),
    'unit'  : 'count',
    'color' : '52/a',
}

metric_info['pgstate_active_clean'] = {
    'title' : _('PGs Active + Clean'),
    'unit'  : 'count',
    'color' : indexed_color(1, 5),
}

metric_info['pgstate_active_scrubbing'] = {
    'title' : _('PGs Active + Scrubbing'),
    'unit'  : 'count',
    'color' : indexed_color(2, 5),
}    

metric_info['pgstate_active_clean_scrubbing'] = {
    'title' : _('PGs Active + Clean + Scrubbing '),
    'unit'  : 'count',
    'color' : indexed_color(3, 5),
}    

metric_info['pgstate_active_clean_scrubbing_deep'] = {
    'title' : _('PGs Active + Clean + Deep Scrubbing '),
    'unit'  : 'count',
    'color' : indexed_color(4, 5),
}    

metric_info['pgstate_active_undersized_degraded'] = {
    'title' : _('PGs Active + Undersized + Degraded'),
    'unit'  : 'count',
    'color' : indexed_color(5, 5),
}

metric_info['pgstates'] = {
    'title' : _('Placement Groups'),
    'unit'  : 'count',
    'color' : '53/a',
}

check_metrics["check_mk-cephstatus"] = df_translation
check_metrics["check_mk-cephstatus"]['num_objects'] = {}
check_metrics["check_mk-cephstatus"]['num_pgs'] = {}
check_metrics["check_mk-cephstatus"]['pgstates'] = { 'name': 'pgstates' }
check_metrics["check_mk-cephstatus"]['~pgstate_.*'] = {}

check_metrics["check_mk-cephdf"] = df_translation
check_metrics["check_mk-cephdf"]["num_objects"] = {}
check_metrics["check_mk-cephdf"]["disk_read_ios"] = {}
check_metrics["check_mk-cephdf"]["disk_write_ios"] = {}
check_metrics["check_mk-cephdf"]["disk_read_throughput"] = {}
check_metrics["check_mk-cephdf"]["disk_write_throughput"] = {}

check_metrics["check_mk-cephosd"] = df_translation

#graph_info['pgstates'] = {
#    'title'  : _('Placement Groups'),
#    'metrics': [
#        ( 'num_pgs', 'line', _('Total') ),
#        ( 'pgstate_active_clean', 'area', _('Active+Clean') ),
#        ( 'pgstate_active_scrubbing', 'stack', _('Active+Scrubbing') ),
#        ( 'pgstate_active_undersized_degraded', 'stack', _('Active+Undersized+Degraded') ),
#        ],
#    'range'  : (0, 'num_pgs:max'),
#}
