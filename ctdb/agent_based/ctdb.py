#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2025 Heinlein Consulting GmbH
#          Robert Sander <r.sander@heinlein-support.de>

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2. This file is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.


from collections.abc import Mapping # pyright: ignore[reportShadowedImports]
from dataclasses import dataclass # pyright: ignore[reportShadowedImports]
from typing import Any, TypedDict # pyright: ignore[reportShadowedImports]

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    RuleSetType,
    Service,
    State,
    StringTable,
)

@dataclass
class CtdbInfo():
    node: str
    ip: str
    disconnected: bool
    unknown: bool
    banned: bool
    disabled: bool
    unhealthy: bool
    stopped: bool
    inactive: bool
    partiallyonline: bool
    thisnode: bool

Section = Mapping[str, CtdbInfo]

def parse_ctdb(string_table: StringTable) -> Section:
    parsed = {}

    try:    
        for x, node, ip, disconnected, unknown, banned, disabled, unhealthy, stopped, inactive, partiallyonline, thisnode, y in string_table:
            if node == "Node":
                continue
            
            parsed[ip] = CtdbInfo(
                node,
                ip,
                disconnected=="1",
                unknown=="1",
                banned=="1",
                disabled=="1",
                unhealthy=="1",
                stopped=="1",
                inactive=="1",
                partiallyonline=="1",
                thisnode=="Y",
            )
    except ValueError:
        pass

    return parsed

agent_section_ctdb = AgentSection(
    name="ctdb",
    parse_function=parse_ctdb,
)

def discovery_ctdb(section: Section) -> DiscoveryResult:
    for ip in section:
        yield Service(item=ip)
        
def check_ctdb(item: str, section: Section) -> CheckResult:
    if item in section:
        data = section[item]

        yield Result(state=State.OK, summary=f"Node {data.node}")

        if data.thisnode:
            yield Result(state=State.OK, summary="this node")

        for a in ["disconnected", "unknown", "banned", "disabled", "unhealthy", "stopped", "inactive", "partiallyonline"]:
            if getattr(data, a):
                yield Result(state=State.CRIT, summary=a)

check_plugin_ctdb = CheckPlugin(
    name="ctdb",
    sections=["ctdb"],
    service_name="CTDB %s",
    discovery_function=discovery_ctdb,
    check_function=check_ctdb,
)
