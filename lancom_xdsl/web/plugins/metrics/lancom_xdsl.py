#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

metric_info["signal_noise_up"] = {
    "title": _("Signal/Noise ratio UP"),
    "unit": "db",
    "color": "#0080e0",
}

metric_info["signal_noise_down"] = {
    "title": _("Signal/Noise ratio DOWN"),
    "unit": "db",
    "color": "#00e060",
}

metric_info["attenuation_up"] = {
    "title": _("Attenuation UP"),
    "unit": "db",
    "color": "#0080e0",
}

metric_info["attenuation_down"] = {
    "title": _("Attenuation DOWN"),
    "unit": "db",
    "color": "#00e060",
}

graph_info["signal_noise_up_down"] = {
    "title": _("Signal/Noise ratio"),
    "metrics": [
        ("signal_noise_down", "line"),
        ("signal_noise_up", "-line"),
    ],
    "scalars": [
        ("signal_noise_down:warn", _("Warning (down)")),
        ("signal_noise_down:crit", _("Critical (down)")),
        ("signal_noise_up:warn,-1,*", _("Warning (up)")),
        ("signal_noise_up:crit,-1,*", _("Critical (up)")),
    ],
}

graph_info["attenuation_up_down"] = {
    "title": _("Attenuation"),
    "metrics": [
        ("attenuation_down", "line"),
        ("attenuation_up", "-line"),
    ],
    "scalars": [
        ("attenuation_down:warn", _("Warning (down)")),
        ("attenuation_down:crit", _("Critical (down)")),
        ("attenuation_up:warn,-1,*", _("Warning (up)")),
        ("attenuation_up:crit,-1,*", _("Critical (up)")),
    ],
}
