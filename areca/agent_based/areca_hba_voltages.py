#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# +------------------------------------------------------------------+
# |             ____ _               _        __  __ _  __           |
# |            / ___| |__   ___  ___| | __   |  \/  | |/ /           |
# |           | |   | '_ \ / _ \/ __| |/ /   | |\/| | ' /            |
# |           | |___| | | |  __/ (__|   <    | |  | | . \            |
# |            \____|_| |_|\___|\___|_|\_\___|_|  |_|_|\_\           |
# |                                                                  |
# +------------------------------------------------------------------+
#
# This file is an addon for Check_MK.
#
# check_mk is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.



# A check for hardware stuff on Areca raid controllers.

# Voltages and battery
#.1.3.6.1.4.1.18928.1.2.2.1.8.1.1.1 = INTEGER: 1
#.1.3.6.1.4.1.18928.1.2.2.1.8.1.1.2 = INTEGER: 2
#.1.3.6.1.4.1.18928.1.2.2.1.8.1.1.3 = INTEGER: 3
#.1.3.6.1.4.1.18928.1.2.2.1.8.1.1.4 = INTEGER: 4
#.1.3.6.1.4.1.18928.1.2.2.1.8.1.1.5 = INTEGER: 5
#.1.3.6.1.4.1.18928.1.2.2.1.8.1.1.6 = INTEGER: 6
#.1.3.6.1.4.1.18928.1.2.2.1.8.1.1.7 = INTEGER: 7
#.1.3.6.1.4.1.18928.1.2.2.1.8.1.1.8 = INTEGER: 8
#.1.3.6.1.4.1.18928.1.2.2.1.8.1.1.9 = INTEGER: 9
#.1.3.6.1.4.1.18928.1.2.2.1.8.1.2.1 = STRING: "12V"
#.1.3.6.1.4.1.18928.1.2.2.1.8.1.2.2 = STRING: "5V"
#.1.3.6.1.4.1.18928.1.2.2.1.8.1.2.3 = STRING: "3.3V"
#.1.3.6.1.4.1.18928.1.2.2.1.8.1.2.4 = STRING: "DDR-II +1.8V"
#.1.3.6.1.4.1.18928.1.2.2.1.8.1.2.5 = STRING: "PCI-E  +1.8V"
#.1.3.6.1.4.1.18928.1.2.2.1.8.1.2.6 = STRING: "CPU    +1.8V"
#.1.3.6.1.4.1.18928.1.2.2.1.8.1.2.7 = STRING: "CPU    +1.2V"
#.1.3.6.1.4.1.18928.1.2.2.1.8.1.2.8 = STRING: "DDR-II +0.9V"
#.1.3.6.1.4.1.18928.1.2.2.1.8.1.2.9 = STRING: "Battery Status"
#.1.3.6.1.4.1.18928.1.2.2.1.8.1.3.1 = INTEGER: 11977
#.1.3.6.1.4.1.18928.1.2.2.1.8.1.3.2 = INTEGER: 5026
#.1.3.6.1.4.1.18928.1.2.2.1.8.1.3.3 = INTEGER: 3296
#.1.3.6.1.4.1.18928.1.2.2.1.8.1.3.4 = INTEGER: 1808
#.1.3.6.1.4.1.18928.1.2.2.1.8.1.3.5 = INTEGER: 1808
#.1.3.6.1.4.1.18928.1.2.2.1.8.1.3.6 = INTEGER: 1824
#.1.3.6.1.4.1.18928.1.2.2.1.8.1.3.7 = INTEGER: 1184
#.1.3.6.1.4.1.18928.1.2.2.1.8.1.3.8 = INTEGER: 896
#.1.3.6.1.4.1.18928.1.2.2.1.8.1.3.9 = INTEGER: 255

# Turn this into something much sweeter.
# The battery status doesnt really belong in here.
#{'voltages': {'12V': 11977,
#              'Battery Status': 255,
#              '5V': 5053,
#              'PCI-E  +1.8V': 1808}}

from cmk.agent_based.v2 import (
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    State,
    startswith,
)
from cmk.plugins.lib.elphase import check_elphase, ElPhase, ReadingState, ReadingWithState


def parse_areca_hba_voltages(string_table):
    epsilon = 10 # allowed deviation in percent
    section = {}
    for id, desc, value in string_table:
        try:
            rated = float(desc.split()[-1].replace("V", ""))
        except ValueError:
            rated = None
        section[id] = {
            "desc": desc,
            "rated": rated,
            "value": float(value) / 1000.0,
        }
        if rated:
            section[id]["rated_lower"] =  rated - rated / 100 * epsilon
            section[id]["rated_upper"] = rated + rated / 100 * epsilon
    return section

def discover_areca_hba_voltages(section) -> DiscoveryResult:
    for id in section.keys():
        yield Service(item=id)

def check_areca_hba_voltages(item, params, section) -> CheckResult:
    if item in section:
        epsilon = 10
        yield Result(state=State.OK, summary=section[item]["desc"])
        voltage = section[item]["value"]
        rated = section[item]["rated"]
        if rated:
            if voltage < section[item]["rated_lower"] or voltage > section[item]["rated_upper"]:
                voltage = (voltage, (1, "Voltage is out of range (%.1f V - %.1f V)" % (section[item]["rated_lower"], section[item]["rated_upper"])))
        data = {
            "voltage": voltage,
        }
        yield from check_elphase(params, ElPhase.from_dict(data))

snmp_section_areca_hba_voltages = SimpleSNMPSection(
    name="areca_hba_voltages",
    parse_function=parse_areca_hba_voltages,
    detect = startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.18928.1"),
    fetch = SNMPTree(
        base=".1.3.6.1.4.1.18928.1.2.2.1.8.1",
        oids=[
            "1", # ARECA-SNMP-MIB::hwControllerBoardVolIndex
            "2", # ARECA-SNMP-MIB::hwControllerBoardVolDesc
            "3", # ARECA-SNMP-MIB::hwControllerBoardVolValue
        ],
    ),
)

check_plugin_areca_hba_voktages = CheckPlugin(
    name="areca_hba_voltages",
    sections=["areca_hba_voltages"],
    service_name="Voltage %s",
    discovery_function=discover_areca_hba_voltages,
    check_function=check_areca_hba_voltages,
    check_default_parameters={},
    check_ruleset_name="el_inphase",
)