
#if_translation.update({
#    "in_avg_15"        : { "name": "if_in_bps", "scale": 8 },
#    "out_avg_15"       : { "name": "if_out_bps", "scale": 8 },
#})

metric_info["in_avg_15"] = {
    "title" : _("Average input bandwidth (15 min)"),
    "unit"  : "bytes/s",
    "color" : "#00e060",
}

metric_info["out_avg_15"] = {
    "title" : _("Average output bandwidth (15 min)"),
    "unit"  : "bytes/s",
    "color" : "#0080e0",
}

graph_info["bandwidth_avg_15"] = {
    "title" : _("Average bandwidth (15 min)"),
    "metrics" : [
        ( "in_avg_15",   "area", ),
        ( "out_avg_15",  "-area", ),
    ],
}

