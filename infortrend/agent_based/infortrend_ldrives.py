#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2013 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>
# (c) 2024 Jens Maus <mail@jens-maus.de>
#

from cmk.agent_based.v2 import (
    exists,
    CheckPlugin,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    State,
    StringTable,
)

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

def inventory_infortrend_ldrives(section):
    for id, status in section:
        yield Service(item=id, parameters={"status": status})

def check_infortrend_ldrives(item, section):
    status_info = { 
        0   : "Good",
        1   : "Rebuilding",
        2   : "Initializing",
        3   : "Degraded",
        4   : "Dead",
        5   : "Invalid",
        6   : "Incomplete",
        7   : "Drive Missing",
        }
    for slot, status in section:
        status = int(status)
        if slot == item:
            output = []
            if status & 128 == 128:
                output.append("Logical Drive Off-line (RW)")
                status = status & 127
                rc = State.UNKNOWN
            if status not in status_info.keys():
                yield Result(state=State.UNKNOWN, summary="Status is %d" % status)
                return
            output.append(status_info[status])
            if status == 0:
                rc = State.OK
            if status == 1 or status == 2:
                rc = State.WARN
            if status > 2:
                rc = State.CRIT
            yield Result(state=rc, summary=", ".join(output))
            return
    yield Result(state=State.UNKNOWN, summary="not yet implemented")

def parse_infortrend_ldrives(string_table: StringTable) -> StringTable | None:
    return string_table or None

snmp_section_infortrend_ldrives = SimpleSNMPSection(
    name="infortrend_ldrives",
    parse_function=parse_infortrend_ldrives,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.1714.1.2.1",
        oids=["2", "6"],
    ),
    detect=exists(".1.3.6.1.4.1.1714.1.1.1.1.0"),
)

check_plugin_infortrend_ldrives = CheckPlugin(
    name="infortrend_ldrives",
    sections=["infortrend_ldrives"],
    service_name="IFT Logical Drive %s",
    discovery_function=inventory_infortrend_ldrives,
    check_function=check_infortrend_ldrives,
#    check_ruleset_name="infortend_ldrives",
)
