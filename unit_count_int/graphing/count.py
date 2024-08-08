#!/usr/bin/env python3

from cmk.graphing.v1 import Title
from cmk.graphing.v1.metrics import Metric, Unit, DecimalNotation, Color

metric_count = Metric(
    name = "count",
    title = Title("Count"),
    unit = Unit(DecimalNotation("")),
    color = Color.DARK_GRAY
)
