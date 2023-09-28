#!/usr/bin/env python3

unit_info["count_int"] = {
    "title": _("Count"),
    "symbol": "",
    "render": lambda v: "%d" % v,
    "stepping": "integer",  # for vertical graph labels
}

metric_info["count"] = {
    "title": _("Count"),
    "unit": "count_int",
    "color": "51",
}
