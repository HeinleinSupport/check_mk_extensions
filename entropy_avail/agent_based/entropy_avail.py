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

from .agent_based_api.v1.type_defs import (
    CheckResult,
    DiscoveryResult,
    HostLabelGenerator,
)

from .agent_based_api.v1 import (
    check_levels,
    register,
    Result,
    State,
    HostLabel,
    Service,
    )

def parse_entropy_avail(string_table):
    section = {}
    for line in string_table:
        try:
            section[line[0]] = int(line[1])
        except ValueError:
            pass
    return section

register.agent_section(
    name="entropy_avail",
    parse_function=parse_entropy_avail,
)

def discovery_entropy_avail(section) -> DiscoveryResult:
    if 'entropy_avail' in section and 'poolsize' in section:
        yield Service()

def _render_bits(bits):
    return "%d bits" % bits

def check_entropy_avail(params, section) -> CheckResult:
    if 'entropy_avail' in section and 'poolsize' in section:
        warn_perc = 0
        crit_perc = 0
        warn_abs  = 0
        crit_abs  = 0

        if isinstance(params, dict):
            if params.has_key('percentage'):
                warn_perc = section['poolsize'] / 100 * params['percentage'][0]
                crit_perc = section['poolsize'] / 100 * params['percentage'][1]
            if params.has_key('absolute'):
                warn_abs  = params['absolute'][0]
                crit_abs  = params['absolute'][1]
        warn = warn_perc if warn_perc > warn_abs else warn_abs
        crit = crit_perc if crit_perc > crit_abs else crit_abs

        yield from check_levels(section['entropy_avail'],
                                levels_lower=(warn, crit),
                                boundaries=(0, section['poolsize']),
                                metric_name="entropy",
                                label="Pool size: %s, Entropy available" % _render_bits(section['poolsize']),
                                render_func=_render_bits)

register.check_plugin(
    name="entropy_avail",
    service_name="Entropy Available",
    sections=["entropy_avail"],
    discovery_function=discovery_entropy_avail,
    check_function=check_entropy_avail,
    check_default_parameters={
        "percentage" : ( 0.0, 0.0 ),
        "absolute" : (200, 100),
    },
    check_ruleset_name="entropy_avail",
)
