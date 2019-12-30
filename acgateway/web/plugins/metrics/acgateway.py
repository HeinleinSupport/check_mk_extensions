#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2019 Heinlein Support GmbH
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

_acgateway_sipperf_info = {
        0:  ("sip_calls_attempted", "Number of Attempted SIP/H323 calls"),
        1:  ("sip_calls_established", "Number of established (connected and voice activated) SIP/H323 calls"),
        2:  ("sip_destination_busy", "Number of Destination Busy SIP/H323 calls"),
        3:  ("sip_no_answer", "Number of No Answer SIP/H323 calls"),
        4:  ("sip_no_route", "Number of No Route SIP/H323 calls. Most likely to be due to wrong number"),
        5:  ("sip_no_capability", "Number of No capability match between peers on SIP/H323 calls"),
        6:  ("sip_failed", "Number of failed SIP/H323 calls"),
        7:  ("sip_fax_attempted", "Number of Attempted SIP/H323 fax calls"),
        8:  ("sip_fax_success", "Number of SIP/H323 fax success calls"),
        9:  ("sip_total_duration", "total duration of SIP/H323 calls"),
}

_acgateway_call_metrics = []
_acgateway_total_metrics = []

for idx, prefix in enumerate([ 'tel2ip', 'ip2tel' ]):
    switch = ''
    if idx % 2:
        switch = '-'
    for key, info in _acgateway_sipperf_info.iteritems():
        metric_name = '%s_%s' % (prefix, info[0])
        if key == 9:
            metric_info[metric_name] = {
                'title' : "%s %s" % ( prefix,_(info[1])),
                'unit'  : 'count',
                'color' : indexed_color(idx*10 + key, 20),
                }
            _acgateway_total_metrics.append( ( metric_name, '%sline' % switch, "%s %s" % ( prefix, _(info[1]) ) ) )
        else:
            metric_info[metric_name] = {
                'title' : "%s %s" % ( prefix,_(info[1])),
                'unit'  : '1/s',
                'color' : indexed_color(idx*10 + key, 20),
                }
            _acgateway_call_metrics.append( ( metric_name, '%sline' % switch, "%s %s" % ( prefix, _(info[1]) ) ) )

graph_info.append({
    'title'  : _('SIP Statistics'),
    'metrics': _acgateway_call_metrics,
})

graph_info.append({
    'title'  : _('SIP Totals'),
    'metrics': _acgateway_total_metrics,
})

