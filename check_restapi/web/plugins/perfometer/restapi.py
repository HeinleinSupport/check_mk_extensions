#!/usr/bin/env python3

from cmk.gui.views.perfometer.legacy_perfometers.active_checks import perfometer_check_http

perfometers["check_mk_active-restapi"] = perfometer_check_http
