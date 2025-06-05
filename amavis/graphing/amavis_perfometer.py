#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.graphing.v1 import perfometers

perfometer_amavis = perfometers.Perfometer(
    name="amavis",
    focus_range=perfometers.FocusRange(
        lower=perfometers.Closed(
            value=0.0,
        ),
        upper=perfometers.Closed(
            value=100.0,
        ),
    ),
    segments=["amavis_child_busy"],
)