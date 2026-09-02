#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2020 Heinlein Support GmbH
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

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Service,
    check_levels,
    render,
    StringTable,
)


def parse_msexch_database_size(string_table: StringTable) -> dict | None:
    section: dict[str, dict[str, int]] = {}
    for line in string_table:
        name = line[0].strip('"')
        if name == "Name":
            continue
        values: dict[str, int] = {}
        sizestr = line[1].strip('"')
        size = int(sizestr.split("(")[1].split(" ")[0].replace(",", ""))
        values["size"] = size
        if len(line) > 2:
            availspacestr = line[2].strip('"')
            available_space = int(availspacestr.split("(")[1].split(" ")[0].replace(",", ""))
            values["availSpace"] = available_space
        section[name] = values

    return section or None


def discover_msexch_database_size(section: dict) -> DiscoveryResult:
    for instance in section:
        yield Service(item=instance)


def _migrate_params(params: dict) -> dict:
    """Migrate legacy parameter format to v2 SimpleLevels format."""
    migrated = {}
    for key in ("size", "availSpace"):
        value = params.get(key)
        if value is None:
            migrated[key] = None
        elif isinstance(value, tuple) and len(value) == 2 and isinstance(value[0], str):
            # Already in new format: ("fixed", (warn, crit)) or ("no_levels", None)
            migrated[key] = value
        elif isinstance(value, tuple) and len(value) == 2:
            # Legacy format: (warn, crit) -> ("fixed", (warn, crit))
            migrated[key] = ("fixed", value)
        else:
            migrated[key] = value
    return migrated


def check_msexch_database_size(item: str, params: dict, section: dict) -> CheckResult:
    values = section.get(item)
    if values is None:
        return

    migrated = _migrate_params(params)

    yield from check_levels(
        values["size"],
        metric_name="database_size",
        levels_upper=migrated["size"],
        render_func=render.disksize,
        label="Size",
    )

    if "availSpace" in values:
        avail_space = values["availSpace"]
        avail_space_pct = avail_space * 100 / values["size"]
        avail_size_str = render.disksize(avail_space)
        yield from check_levels(
            avail_space_pct,
            metric_name="availableNewMailboxSpace",
            levels_upper=migrated["availSpace"],
            render_func=lambda v: f"{avail_size_str} ({render.percent(v)})",
            label="Available New Mailbox Space",
            boundaries=(0.0, 100.0),
        )


agent_section_msexch_database_size = AgentSection(
    name="msexch_database_size",
    parse_function=parse_msexch_database_size,
)

check_plugin_msexch_database_size = CheckPlugin(
    name="msexch_database_size",
    service_name="Exchange Database Size %s",
    sections=["msexch_database_size"],
    discovery_function=discover_msexch_database_size,
    check_function=check_msexch_database_size,
    check_default_parameters={
        "size": None,
        "availSpace": ("fixed", (20.0, 40.0)),
    },
    check_ruleset_name="msexch_database_size",
)
