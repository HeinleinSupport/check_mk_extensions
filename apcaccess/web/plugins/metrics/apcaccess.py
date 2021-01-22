#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

metric_info["timeleft"] = {
    "title" : _("Battery Runtime"),
    "unit"  : "s",
    "color" : "#80f000",
}

graph_info["battery_capacity"] = {
    "metrics" : [
        ( "battery_capacity", "area" ),
    ],
    "scalars" : [
        ( "battery_capacity:crit",     _("Critical")),
        ( "battery_capacity:warn",     _("Warning")),
    ],
    "range" : (0,100),
}

