#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2013 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  This file is distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    check_levels,
    DiscoveryResult,
    Service,
    StringTable,
)

from collections.abc import Mapping # type: ignore
from typing import Any # type: ignore

Section = Mapping[str, Any]

def parse_entropy_avail(string_table: StringTable) -> Section:
    section = {}
    for line in string_table:
        try:
            section[line[0]] = int(line[1])
        except ValueError:
            pass
    return section

agent_section_entropy_avail = AgentSection(
    name="entropy_avail",
    parse_function=parse_entropy_avail,
)

def discovery_entropy_avail(section: Section) -> DiscoveryResult:
    if 'entropy_avail' in section and 'poolsize' in section:
        yield Service()

def _render_bits(bits):
    return "%d bits" % bits

def check_entropy_avail(params, section: Section) -> CheckResult:
    if 'entropy_avail' in section and 'poolsize' in section:

        levels_lower = None
        warn_perc = 0
        crit_perc = 0
        warn_abs  = 0
        crit_abs  = 0

        if "percentage" in params and params["percentage"][0] == "fixed":
            warn_perc = section['poolsize'] / 100 * params['percentage'][1][0]
            crit_perc = section['poolsize'] / 100 * params['percentage'][1][1]
        if "absolute" in params and params["absolute"][0] == "fixed":
            warn_abs  = params['absolute'][1][0]
            crit_abs  = params['absolute'][1][1]
        warn = warn_perc if warn_perc > warn_abs else warn_abs
        crit = crit_perc if crit_perc > crit_abs else crit_abs
        
        if warn and crit:
            levels_lower = ("fixed", (warn, crit))

        yield from check_levels(section['entropy_avail'],
                                levels_lower=levels_lower,
                                boundaries=(0, section['poolsize']),
                                metric_name="entropy",
                                label="Pool size: %s, Entropy available" % _render_bits(section['poolsize']),
                                render_func=_render_bits)

check_plugin_entropy_avail = CheckPlugin(
    name="entropy_avail",
    service_name="Entropy Available",
    sections=["entropy_avail"],
    discovery_function=discovery_entropy_avail,
    check_function=check_entropy_avail,
    check_default_parameters={
        "percentage" : ("fixed", (0.0, 0.0)),
        "absolute" : ("fixed", (200, 100)),
    },
    check_ruleset_name="entropy_avail",
)
