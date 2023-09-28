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

metric_info['ipneigh_total'] = {
    'title': _('Neighbors Total'),
    'unit': 'count_int',
    'color': '11/a',
}

metric_info['ipneigh_permanent'] = {
    'title': _('Neighbors Permanent'),
    'unit': 'count_int',
    'color': '12/a',
}

metric_info['ipneigh_noarp'] = {
    'title': _('Neighbors noarp'),
    'unit': 'count_int',
    'color': '13/a',
}

metric_info['ipneigh_reachable'] = {
    'title': _('Neighbors Reachable'),
    'unit': 'count_int',
    'color': '14/a',
}

metric_info['ipneigh_stale'] = {
    'title': _('Neighbors Stale'),
    'unit': 'count_int',
    'color': '21/a',
}

metric_info['ipneigh_none'] = {
    'title': _('Neighbors None'),
    'unit': 'count_int',
    'color': '22/a',
}

metric_info['ipneigh_incomplete'] = {
    'title': _('Neighbors Incomplete'),
    'unit': 'count_int',
    'color': '23/a',
}

metric_info['ipneigh_delay'] = {
    'title': _('Neighbors Delay'),
    'unit': 'count_int',
    'color': '24/a',
}

metric_info['ipneigh_probe'] = {
    'title': _('Neighbors Probe'),
    'unit': 'count_int',
    'color': '15/a',
}

metric_info['ipneigh_failed'] = {
    'title': _('Neighbors Failed'),
    'unit': 'count_int',
    'color': '25/a',
}
