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


from cmk.graphing.v1 import Title, graphs
from cmk.graphing.v1.metrics import (
    Color,
    DecimalNotation,
    IECNotation,
    Metric,
    StrictPrecision,
    TimeNotation,
    Unit,
)

UNIT_METERS_PER_SECOND = Unit(IECNotation("m/s"))
UNIT_TIME = Unit(TimeNotation())
UNIT_PERCENT = Unit(DecimalNotation("%"), StrictPrecision(2))
UNIT_NUMBER = Unit(DecimalNotation(''))
UNIT_COUNT = Unit(DecimalNotation(""), StrictPrecision(0))
UNIT_COUNTER = Unit(DecimalNotation(''), StrictPrecision(2))

metric_tx_jitter = Metric(
    name="tx_jitter",
    title=Title("TX Jitter"),
    unit=UNIT_TIME,
    color=Color.LIGHT_BLUE,
)

metric_rx_jitter = Metric(
    name="rx_jitter",
    title=Title("RX Jitter"),
    unit=UNIT_TIME,
    color=Color.LIGHT_GREEN,
)

metric_tx_latency = Metric(
    name="tx_latency",
    title=Title("TX Latency"),
    unit=UNIT_TIME,
    color=Color.BLUE,
)

metric_rx_latency = Metric(
    name="rx_latency",
    title=Title("RX Latency"),
    unit=UNIT_TIME,
    color=Color.GREEN,
)

metric_arp_entries = Metric(
    name="arp_entries",
    title=Title("ARP Entries"),
    unit=UNIT_COUNT,
    color=Color.CYAN,
)

graph_if_errors = graphs.Bidirectional(
    name='graph_if_errors',
    title=Title('Errors'),
    upper=graphs.Graph(
        name="if_errors_in",
        title=Title("In Errors"),
        simple_lines=["if_in_errors"],
        conflicting=["if_in_discards", "indisc"],
    ),
    lower=graphs.Graph(
        name="if_errors_out",
        title=Title("Out Errors"),
        simple_lines=["if_out_errors"],
        conflicting=["if_out_discards", "outdisc"],
    ),
)

graph_jitter = graphs.Bidirectional(
    name='graph_jitter',
    title=Title('Jitter'),
    upper=graphs.Graph(
        name="rx_jitter",
        title=Title("Jitter In"),
        simple_lines=["rx_jitter"],
    ),
    lower=graphs.Graph(
        name="tx_jitter",
        title=Title("Jitter Out"),
        simple_lines=["tx_jitter"],
    ),
)

graph_latency = graphs.Bidirectional(
    name='graph_latency',
    title=Title('Latency'),
    upper=graphs.Graph(
        name="rx_latency",
        title=Title("Latency In"),
        simple_lines=["rx_latency"],
    ),
    lower=graphs.Graph(
        name="tx_latency",
        title=Title("Latency Out"),
        simple_lines=["tx_latency"],
    ),
)

graph_unicast_packets = graphs.Bidirectional(
    name='graph_unicast_packets',
    title=Title('Unicast Packets'),
    upper=graphs.Graph(
        name="if_in_unicast",
        title=Title("Unicast Packets In"),
        simple_lines=["if_in_unicast"],
        conflicting=["if_in_mcast", "inmcast"],
    ),
    lower=graphs.Graph(
        name="if_out_unicast",
        title=Title("Unicast Packets Out"),
        simple_lines=["if_out_unicast"],
        conflicting=["if_out_mcast", "outmcast"],
    ),
)
