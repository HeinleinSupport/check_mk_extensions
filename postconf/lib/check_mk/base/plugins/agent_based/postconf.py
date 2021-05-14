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

from cmk.utils import debug
from pprint import pprint

from .agent_based_api.v1.type_defs import (
    CheckResult,
    DiscoveryResult,
)

from .agent_based_api.v1 import (
    register,
    Result,
    State,
    Service,
    )

def parse_postconf(string_table):
    section = {}
    for line in string_table:
        if line[1] == '=':
            section[line[0]] = " ".join(line[2:])
    return section

register.agent_section(
    name="postconf",
    parse_function=parse_postconf,
)

def discover_postconf(section) -> DiscoveryResult:
    if section:
        yield Service()

def check_postconf(params, section) -> CheckResult:
    if debug.enabled():
        pprint(params)
        pprint(section)
    if 'config' not in params:
        yield Result (state=State.OK,
                      summary="No Postfix configuration parameters to check.")
    elif not isinstance(params['config'], list):
        yield Result(state=State.UNKNOWN,
                     summary="Parameters not in list form")
    else:
        postconf = {}
        for param in params['config']:
            postconf[param[0]] = param[1]

        for key, value in section.items():
            if key in postconf:
                if value == postconf[key]:
                    yield Result(state=State.OK,
                                 summary="%s=%s" % (key, value))
                else:
                    yield Result(state=State.WARN,
                                 summary="%s=%s, %s expected" % (key, value, postconf[key]))
                del(postconf[key])
        for key in postconf:
            yield Result(state=State.UNKNOWN,
                         summary="%s not found" % key)

register.check_plugin(
    name="postconf",
    service_name="Postfix Config",
    sections=["postconf"],
    discovery_function=discover_postconf,
    check_function=check_postconf,
    check_default_parameters={
        'config': [ ( 'soft_bounce', 'no' ) ],
    },
    check_ruleset_name="postconf",
)

