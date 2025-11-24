#!/usr/bin/env python3
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

from cmk.graphing.v1 import Title, graphs, metrics

UNIT_COUNTER = metrics.Unit(metrics.DecimalNotation(''), metrics.StrictPrecision(2))
UNIT_PERCENTAGE = metrics.Unit(metrics.DecimalNotation('%'))
UNIT_PER_SECOND = metrics.Unit(metrics.DecimalNotation('/s'))
UNIT_TIME = metrics.Unit(metrics.TimeNotation())

metric_active_alarms = metrics.Metric(name='active_alarms', title=Title("Active Alarms"), unit=UNIT_COUNTER, color=metrics.Color.YELLOW,)
metric_active_calls = metrics.Metric(name='active_calls', title=Title("Active Calls"), unit=UNIT_COUNTER, color=metrics.Color.CYAN,)
metric_archived_alarms = metrics.Metric(name='archived_alarms', title=Title("Archived Alarms"), unit=UNIT_COUNTER, color=metrics.Color.DARK_YELLOW,)
metric_average_call_duration = metrics.Metric(name='average_call_duration', title=Title("Average Call Duration"), unit=UNIT_TIME, color=metrics.Color.CYAN,)
metric_average_success_ratio = metrics.Metric(name='average_success_ratio', title=Title("Average Success Ratio"), unit=UNIT_PERCENTAGE, color=metrics.Color.CYAN,)
metric_calls_per_sec = metrics.Metric(name='calls_per_sec', title=Title("Calls per Second"), unit=UNIT_PER_SECOND, color=metrics.Color.CYAN,)
metric_ip2tel_sip_calls_attempted = metrics.Metric(name='ip2tel_sip_calls_attempted', title=Title("ip2tel Number of Attempted SIP/H323 calls"), unit=UNIT_PER_SECOND, color=metrics.Color.CYAN,)
metric_ip2tel_sip_calls_established = metrics.Metric(name='ip2tel_sip_calls_established', title=Title("ip2tel Number of established (connected and voice activated) SIP/H323 calls"), unit=UNIT_PER_SECOND, color=metrics.Color.DARK_BLUE,)
metric_ip2tel_sip_destination_busy = metrics.Metric(name='ip2tel_sip_destination_busy', title=Title("ip2tel Number of Destination Busy SIP/H323 calls"), unit=UNIT_PER_SECOND, color=metrics.Color.LIGHT_ORANGE,)
metric_ip2tel_sip_failed = metrics.Metric(name='ip2tel_sip_failed', title=Title("ip2tel Number of failed SIP/H323 calls"), unit=UNIT_PER_SECOND, color=metrics.Color.ORANGE,)
metric_ip2tel_sip_fax_attempted = metrics.Metric(name='ip2tel_sip_fax_attempted', title=Title("ip2tel Number of Attempted SIP/H323 fax calls"), unit=UNIT_PER_SECOND, color=metrics.Color.YELLOW,)
metric_ip2tel_sip_fax_success = metrics.Metric(name='ip2tel_sip_fax_success', title=Title("ip2tel Number of SIP/H323 fax success calls"), unit=UNIT_PER_SECOND, color=metrics.Color.BLUE,)
metric_ip2tel_sip_no_answer = metrics.Metric(name='ip2tel_sip_no_answer', title=Title("ip2tel Number of No Answer SIP/H323 calls"), unit=UNIT_PER_SECOND, color=metrics.Color.DARK_YELLOW,)
metric_ip2tel_sip_no_capability = metrics.Metric(name='ip2tel_sip_no_capability', title=Title("ip2tel Number of No capability match between peers on SIP/H323 calls"), unit=UNIT_PER_SECOND, color=metrics.Color.DARK_PURPLE,)
metric_ip2tel_sip_no_route = metrics.Metric(name='ip2tel_sip_no_route', title=Title("ip2tel Number of No Route SIP/H323 calls. Most likely to be due to wrong number"), unit=UNIT_PER_SECOND, color=metrics.Color.DARK_BLUE,)
metric_ip2tel_sip_total_duration = metrics.Metric(name='ip2tel_sip_total_duration', title=Title("ip2tel total duration of SIP/H323 calls"), unit=UNIT_TIME, color=metrics.Color.DARK_PURPLE,)
metric_rx_trans = metrics.Metric(name='rx_trans', title=Title("RX Transactions per Second"), unit=UNIT_PER_SECOND, color=metrics.Color.DARK_PURPLE,)
metric_tel2ip_sip_calls_attempted = metrics.Metric(name='tel2ip_sip_calls_attempted', title=Title("tel2ip Number of Attempted SIP/H323 calls"), unit=UNIT_PER_SECOND, color=metrics.Color.DARK_PURPLE,)
metric_tel2ip_sip_calls_established = metrics.Metric(name='tel2ip_sip_calls_established', title=Title("tel2ip Number of established (connected and voice activated) SIP/H323 calls"), unit=UNIT_PER_SECOND, color=metrics.Color.YELLOW,)
metric_tel2ip_sip_destination_busy = metrics.Metric(name='tel2ip_sip_destination_busy', title=Title("tel2ip Number of Destination Busy SIP/H323 calls"), unit=UNIT_PER_SECOND, color=metrics.Color.CYAN,)
metric_tel2ip_sip_failed = metrics.Metric(name='tel2ip_sip_failed', title=Title("tel2ip Number of failed SIP/H323 calls"), unit=UNIT_PER_SECOND, color=metrics.Color.CYAN,)
metric_tel2ip_sip_fax_attempted = metrics.Metric(name='tel2ip_sip_fax_attempted', title=Title("tel2ip Number of Attempted SIP/H323 fax calls"), unit=UNIT_PER_SECOND, color=metrics.Color.LIGHT_BLUE,)
metric_tel2ip_sip_fax_success = metrics.Metric(name='tel2ip_sip_fax_success', title=Title("tel2ip Number of SIP/H323 fax success calls"), unit=UNIT_PER_SECOND, color=metrics.Color.DARK_PINK,)
metric_tel2ip_sip_no_answer = metrics.Metric(name='tel2ip_sip_no_answer', title=Title("tel2ip Number of No Answer SIP/H323 calls"), unit=UNIT_PER_SECOND, color=metrics.Color.BLUE,)
metric_tel2ip_sip_no_capability = metrics.Metric(name='tel2ip_sip_no_capability', title=Title("tel2ip Number of No capability match between peers on SIP/H323 calls"), unit=UNIT_PER_SECOND, color=metrics.Color.DARK_YELLOW,)
metric_tel2ip_sip_no_route = metrics.Metric(name='tel2ip_sip_no_route', title=Title("tel2ip Number of No Route SIP/H323 calls. Most likely to be due to wrong number"), unit=UNIT_PER_SECOND, color=metrics.Color.PINK,)
metric_tel2ip_sip_total_duration = metrics.Metric(name='tel2ip_sip_total_duration', title=Title("tel2ip total duration of SIP/H323 calls"), unit=UNIT_TIME, color=metrics.Color.YELLOW,)
metric_tx_trans = metrics.Metric(name='tx_trans', title=Title("TX Transactions per Second"), unit=UNIT_PER_SECOND, color=metrics.Color.PURPLE,)

graph_sip_statistics = graphs.Bidirectional(name='sip_statistics', title=Title("SIP Statistics"), lower=graphs.Graph(name='sip_statistics_lower', title=Title("SIP Statistics"), simple_lines=['ip2tel_sip_calls_attempted', 'ip2tel_sip_calls_established', 'ip2tel_sip_destination_busy', 'ip2tel_sip_no_answer', 'ip2tel_sip_no_route', 'ip2tel_sip_no_capability', 'ip2tel_sip_failed', 'ip2tel_sip_fax_attempted', 'ip2tel_sip_fax_success',],), upper=graphs.Graph(name='sip_statistics_upper', title=Title("SIP Statistics"), simple_lines=['tel2ip_sip_calls_attempted', 'tel2ip_sip_calls_established', 'tel2ip_sip_destination_busy', 'tel2ip_sip_no_answer', 'tel2ip_sip_no_route', 'tel2ip_sip_no_capability', 'tel2ip_sip_failed', 'tel2ip_sip_fax_attempted', 'tel2ip_sip_fax_success',],),)
graph_sip_totals = graphs.Bidirectional(name='sip_totals', title=Title("SIP Totals"), lower=graphs.Graph(name='sip_totals_lower', title=Title("SIP Totals"), simple_lines=['ip2tel_sip_total_duration'],), upper=graphs.Graph(name='sip_totals_upper', title=Title("SIP Totals"), simple_lines=['tel2ip_sip_total_duration'],),)
graph_transactions = graphs.Bidirectional(name='transactions', title=Title("Transactions per Second"), lower=graphs.Graph(name='transactions_lower', title=Title("Transactions per Second"), compound_lines=['tx_trans'],), upper=graphs.Graph(name='transactions_upper', title=Title("Transactions per Second"), compound_lines=['rx_trans'],),)
