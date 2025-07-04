#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2013 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>
# (c) 2024 Jens Maus <mail@jens-maus.de>
#

from cmk.agent_based.v2 import (
    exists,
    render,
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

def inventory_infortrend_disks(section):
    for line in section:
        yield Service(item=line[0])

def check_infortrend_disks(item, section):
    status_info = { 
        0   : "New Drive",
        1   : "On-Line Drive",
        2   : "Used Drive",
        3   : "Spare Drive",
        4   : "Drive Initialization in Progress",
        5   : "Drive Rebuild in Progress",
        6   : "Add Drive to Logical Drive in Progress",
        9   : "Global Spare Drive",
        17  : "Drive is in process of Cloning another Drive",
        18  : "Drive is a valid Clone of another Drive",
        19  : "Drive is in process of Copying from another Drive (for Copy/Replace LD Expansion function)",
        63  : "Drive Absent",
        128 : "SCSI Device (Type 0)",
        129 : "SCSI Device (Type 1)",
        130 : "SCSI Device (Type 2)",
        131 : "SCSI Device (Type 3)",
        132 : "SCSI Device (Type 4)",
        133 : "SCSI Device (Type 5)",
        134 : "SCSI Device (Type 6)",
        135 : "SCSI Device (Type 7)",
        136 : "SCSI Device (Type 8)",
        137 : "SCSI Device (Type 9)",
        138 : "SCSI Device (Type 10)",
        139 : "SCSI Device (Type 11)",
        140 : "SCSI Device (Type 12)",
        141 : "SCSI Device (Type 13)",
        142 : "SCSI Device (Type 14)",
        143 : "SCSI Device (Type 15)",
        252 : "Missing Global Spare Drive",
        253 : "Missing Spare Drive",
        254 : "Missing Drive",
        255 : "Failed Drive"
        }
    for slot, status, model, version, serial, size, blocksize in section:
        if slot == item:
            status = int(status) if status else 0
            disksize = int(size) * 2 ** int(blocksize)
            info = "%s %s %s, %s, " % (model, version, serial, render.iobandwidth(disksize))
            if status not in status_info.keys():
                yield Result(state=State.UNKNOWN, summary="%sStatus is %d" % (info, status))
                return

            rc = State.WARN
            if status == 1 or status == 3 or status == 9:
                rc = State.OK
            if status > 63:
                rc = State.CRIT
            yield Result(state=rc, summary=info + status_info[status])
            return

def parse_infortrend_disks(string_table: StringTable) -> StringTable | None:
    return string_table or None

snmp_section_infortrend_disks = SimpleSNMPSection(
    name="infortrend_disks",
    parse_function=parse_infortrend_disks,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.1714.1.6.1",
        oids=["13", "11", "15", "16", "17", "7", "8"],
    ),
    detect=exists(".1.3.6.1.4.1.1714.1.1.1.1.0"),
)

check_plugin_infortrend_disks = CheckPlugin(
    name="infortrend_disks",
    sections=["infortrend_disks"],
    service_name="IFT Disk Slot %s",
    discovery_function=inventory_infortrend_disks,
    check_function=check_infortrend_disks,
#    check_ruleset_name="infortend_disks",
)
