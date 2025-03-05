#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2025 Heinlein Support GmbH
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

from cmk.graphing.v1 import Title
from cmk.graphing.v1.metrics import (
    Color,
    DecimalNotation,
    IECNotation,
    Metric,
    StrictPrecision,
    Unit,
)

UNIT_INTEGER = Unit(DecimalNotation(""), StrictPrecision(0))
UNIT_PER_SECOND = Unit(IECNotation("/s"))

#   .--State---------------------------------------------------------------.
#   |                       ____  _        _                               |
#   |                      / ___|| |_ __ _| |_ ___                         |
#   |                      \___ \| __/ _` | __/ _ \                        |
#   |                       ___) | || (_| | ||  __/                        |
#   |                      |____/ \__\__,_|\__\___|                        |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.
metric_sip_sets_out_service = Metric(
    name="sip_sets_out_service",
    title=Title("Sets out of service"),
    unit=UNIT_INTEGER,
    color=Color.RED,
)

metric_sip_sets_in_service = Metric(
    name="sip_sets_in_service",
    title=Title("Sets in service"),
    unit=UNIT_INTEGER,
    color=Color.GREEN,
)

metric_sip_sets_unregistered = Metric(
    name="sip_sets_unregistered",
    title=Title("Sets unregistered"),
    unit=UNIT_INTEGER,
    color=Color.LIGHT_RED,
)

metric_sip_sets_registered = Metric(
    name="sip_sets_registered",
    title=Title("Sets registered"),
    unit=UNIT_INTEGER,
    color=Color.LIGHT_GREEN,
)

#   .--IPDomain------------------------------------------------------------.
#   |            ___ ____  ____                        _                   |
#   |           |_ _|  _ \|  _ \  ___  _ __ ___   __ _(_)_ __              |
#   |            | || |_) | | | |/ _ \| '_ ` _ \ / _` | | '_ \             |
#   |            | ||  __/| |_| | (_) | | | | | | (_| | | | | |            |
#   |           |___|_|   |____/ \___/|_| |_| |_|\__,_|_|_| |_|            |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.
# sip_cac_used;sip_cac_allowed;;sip_dsp_ooo;sip_dsp_avail;sip_conf_ooo;sip_dsp_busy;sip_conf_busy;sip_conf_avail

metric_sip_cac_overruns = Metric(
    name="sip_cac_overruns",
    title=Title("CAC overruns"),
    unit=UNIT_PER_SECOND,
    color=Color.BLUE,
)

metric_sip_dsp_overruns = Metric(
    name="sip_dsp_overruns",
    title=Title("DSP compressors overruns"),
    unit=UNIT_PER_SECOND,
    color=Color.CYAN,
)

#   .--Trunk---------------------------------------------------------------.
#   |                     _____                 _                          |
#   |                    |_   _| __ _   _ _ __ | | __                      |
#   |                      | || '__| | | | '_ \| |/ /                      |
#   |                      | || |  | |_| | | | |   <                       |
#   |                      |_||_|   \__,_|_| |_|_|\_\                      |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.
# ;;sip_chan_busy;sip_chan_free

metric_sip_cumul_overruns = Metric(
    name="sip_cumul_overruns",
    title=Title("Failed outgoing calls"),
    unit=UNIT_PER_SECOND,
    color=Color.DARK_BLUE,
)

metric_sip_cumul_ooss = Metric(
    name="sip_cumul_ooss",
    title=Title("Channels out of service"),
    unit=UNIT_PER_SECOND,
    color=Color.DARK_GRAY,
)