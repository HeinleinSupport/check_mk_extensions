#!/usr/bin/env python3

from cmk.graphing.v1 import Title
from cmk.graphing.v1.metrics import Color, DecimalNotation, Metric, Unit


metric_msexch_available_new_mailbox_space = Metric(
    name="availableNewMailboxSpace",
    title=Title("Available New Mailbox Space"),
    unit=Unit(DecimalNotation("%")),
    color=Color.PURPLE,
)
