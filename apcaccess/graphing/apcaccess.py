#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.graphing.v1 import Title
from cmk.graphing.v1.metrics import (
    Color,
    Metric,
    TimeNotation,
    Unit,
)

UNIT_SECONDS = Unit(TimeNotation())

metric_timeleft = Metric(
    name = "timeleft",
    title = Title("Battery Runtime"),
    unit = UNIT_SECONDS,
    color = Color.LIGHT_GREEN,
)