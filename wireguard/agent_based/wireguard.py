#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2020 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>
#          Matthias Henze <mahescho@gmail.com>

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

from collections.abc import Mapping # type: ignore
from typing import Any # type: ignore

from cmk.agent_based.v2 import (
    AgentSection,
    check_levels,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    get_rate,
    get_value_store,
    Metric,
    render,
    Result,
    RuleSetType,
    Service,
    ServiceLabel,
    State,
    StringTable,
)

import time

Section = Mapping[str, Any]

def parse_wireguard(string_table: StringTable) -> Section:
    section = {}
    interface = None
    for line in string_table:
        if len(line) == 1 and line[0].startswith("[[") and line[0].endswith("]]"):
            interface = line[0][2:-2]
            section[interface] = {}
        if len(line) == 2:
            continue
        if len(line) == 7:
            section[interface][line[0]] = {
                "endpoint": line[1],
                "allowed-ips": line[2],
                "latest-handshake": int(line[3]),
                "transfer-rx": int(line[4]),
                "transfer-tx": int(line[5]),
                "persistent-keepalive": line[6]
            }
    return section

agent_section_wireguard = AgentSection(
    name="wireguard",
    parse_function=parse_wireguard,
)

def discover_wireguard(section: Section) -> DiscoveryResult:
    for interface, peers in section.items():
        yield Service(item="%s" % interface)
        for peer, data in peers.items():
            yield Service(item="%s Peer %s" % (interface, peer))

def check_wireguard(item: str, params, section: Section) -> CheckResult:
    if "Peer" in item:
        interface, x, peer = item.split(" ")
        if interface in section:
            peers = section[interface]
            if peer in peers:
                value_store = get_value_store()
                now = time.time()
                data = peers[peer]
                in_rate = get_rate(
                    value_store,
                    "wireguard.%s.%s.in" % (interface, peer),
                    now,
                    data["transfer-rx"],
                )
                out_rate = get_rate(
                    value_store,
                    "wireguard.%s.%s.out" % (interface, peer),
                    now,
                    data["transfer-tx"],
                )
                yield Result(state=State.OK,
                             summary="endpoint: %s" % data["endpoint"])
                yield Result(state=State.OK,
                             summary="allowed IPs: %s" % data["allowed-ips"])
                yield Metric("if_in_octets", in_rate)
                yield Metric("if_out_octets", out_rate)
                if data["latest-handshake"] > 0:
                    since = now - data["latest-handshake"]
                    yield from check_levels(
                        value=since,
                        levels_upper=params.get("timeout"),
                        metric_name="last_updated",
                        label="Latest Handshake",
                        render_func=render.timespan,
                    )
                else:
                    yield Result(state=State.OK,
                                 summary="never connected")
    else:
        if item in section:
            timeout = params.get("timeout", ("no_levels", None))
            peers = section[item]
            numpeers = len(peers)
            activepeers = 0
            now = time.time()
            for peer, data in peers.items():
                if data["latest-handshake"] > 0:
                    since = now - data["latest-handshake"]
                    if timeout[0] == "fixed_levels" and (since < timeout[1][0] or since < timeout[1][1]):
                        activepeers += 1
                    if timeout[0] == "no_levels":
                        activepeers += 1
            yield Result(state=State.OK,
                         summary="%d configured peer(s)" % numpeers)
            yield Metric("configured_vpn_tunnels", numpeers)
            yield Result(state=State.OK,
                         summary="%d active peer(s)" % activepeers)
            yield Metric("active_vpn_tunnels", activepeers)

check_plugin_wireguard = CheckPlugin(
    name="wireguard",
    service_name="WireGuard %s",
    sections=["wireguard"],
    discovery_function=discover_wireguard,
    check_function=check_wireguard,
    check_default_parameters = {
        "timeout": ("no_levels", None), # disable by default
    },
    check_ruleset_name = "wireguard_data",
)
