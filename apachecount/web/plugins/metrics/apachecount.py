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

metric_info['apachecount_http_sum_100'] = {
    'title': _('HTTP Codes 100 - 199'),
    'unit': '1/s',
    'color': '34/a',
}
for code in range(100, 200):
    metric_info['apachecount_http_%d' % code] = {
        'title': _('HTTP Code %d' % code),
        'unit': '1/s',
        'color': '34/a',
    }

metric_info['apachecount_http_sum_200'] = {
    'title': _('HTTP Codes 200 - 299'),
    'unit': '1/s',
    'color': '32/a',
}
for code in range(200, 300):
    metric_info['apachecount_http_%d' % code] = {
        'title': _('HTTP Code %d' % code),
        'unit': '1/s',
        'color': '32/a',
    }

metric_info['apachecount_http_sum_300'] = {
    'title': _('HTTP Codes 300 - 399'),
    'unit': '1/s',
    'color': '31/a',
}
for code in range(300, 400):
    metric_info['apachecount_http_%d' % code] = {
        'title': _('HTTP Code %d' % code),
        'unit': '1/s',
        'color': '31/a',
    }

metric_info['apachecount_http_sum_400'] = {
    'title': _('HTTP Codes 400 - 499'),
    'unit': '1/s',
    'color': '23/a',
}
for code in range(400, 500):
    metric_info['apachecount_http_%d' % code] = {
        'title': _('HTTP Code %d' % code),
        'unit': '1/s',
        'color': '23/a',
    }

metric_info['apachecount_http_sum_500'] = {
    'title': _('HTTP Codes 500 - 599'),
    'unit': '1/s',
    'color': '14/a',
}
for code in range(500, 600):
    metric_info['apachecount_http_%d' % code] = {
        'title': _('HTTP Code %d' % code),
        'unit': '1/s',
        'color': '14/a',
    }

for code in range(6, 10):
    metric_info['apachecount_http_sum_%d00' % code] = {
        'title': _('HTTP Codes %d00 - %d99' % (code, code)),
        'unit': '1/s',
        'color': '45/a',
    }
for code in range(600, 1000):
    metric_info['apachecount_http_%d' % code] = {
        'title': _('HTTP Code %d' % code),
        'unit': '1/s',
        'color': '45/a',
    }

