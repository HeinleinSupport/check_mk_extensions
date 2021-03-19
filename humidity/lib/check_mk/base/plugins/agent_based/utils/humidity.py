#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2021 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# tails. You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

from ..agent_based_api.v1 import (
    check_levels,
    render,
)

def check_humidity(humidity, params):
    if isinstance(params, dict):
        levels = ((params.get("levels") or (None, None)) + (params.get("levels_lower") or
                                                            (None, None)))
    elif isinstance(params, (list, tuple)):
        # old params = (crit_low , warn_low, warn, crit)
        levels = (params[2], params[3], params[1], params[0])
    else:
        levels = (None, None, None, None)

    yield from check_levels(
        humidity,
        metric_name="humidity",
        levels_upper=(levels[0], levels[1]),
        levels_lower=(levels[2], levels[3]),
        render_func=render.percent,
        boundaries=(0, 100),
    )
