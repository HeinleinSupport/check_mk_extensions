#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#     2021 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>

# +-----------------------------------------------------------------+
# |                                                                 |
# |        (  ___ \     | \    /\|\     /||\     /|( (    /|        |
# |        | (   ) )    |  \  / /| )   ( || )   ( ||  \  ( |        |
# |        | (__/ /     |  (_/ / | |   | || (___) ||   \ | |        |
# |        |  __ (      |   _ (  | |   | ||  ___  || (\ \) |        |
# |        | (  \ \     |  ( \ \ | |   | || (   ) || | \   |        |
# |        | )___) )_   |  /  \ \| (___) || )   ( || )  \  |        |
# |        |/ \___/(_)  |_/    \/(_______)|/     \||/    )_)        |
# |                                                                 |
# | Copyright Bastian Kuhn 2011                mail@bastian-kuhn.de | 
# +-----------------------------------------------------------------+
#
# This file is a check Script for check_mk
# Information about me can be found at http://bastian-kuhn.de
# Information about check_mk at http://mathias-kettner.de/check_mk.
#
# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.


# Example Agent Output
#<<<dir_size>>>
#17516   /tmp/
#626088  /usr/local/

from collections.abc import Mapping # type: ignore
from typing import Any # type: ignore

from cmk.agent_based.v2 import (
    AgentSection,
    check_levels,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    render,
    Service,
    StringTable,
)

from cmk.utils import debug
from pprint import pprint # type: ignore

Section = Mapping[str, Any]


def parse_dir_size(string_table: StringTable) -> Section:
    if debug.enabled():
        pprint(string_table)
    section = {}
    for line in string_table:
        size = int(line[0])
        path = ' '.join(line[1:])
        section[path] = size * 1024
    if debug.enabled():
        pprint(section)
    return section

agent_section_packages = AgentSection(
    name="dir_size",
    parse_function=parse_dir_size,
)


def discover_dir_size(section: Section) -> DiscoveryResult:
    for path in section:
        yield Service(item=path)

def check_dir_size(item: str, params, section: Section) -> CheckResult:
    if item in section:
        yield from check_levels(
            section[item],
            levels_upper=params.get('levels_upper'),
            metric_name="dir_size",
            label="Folder size",
            render_func=render.bytes,
        )

check_plugin_dir_size = CheckPlugin(
    name="dir_size",
    service_name="Size of %s",
    sections=["dir_size"],
    discovery_function=discover_dir_size,
    check_function=check_dir_size,
    check_default_parameters={},
    check_ruleset_name="dir_size",
)
