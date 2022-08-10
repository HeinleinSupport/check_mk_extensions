#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2022 Heinlein Consulting GmbH
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

from .agent_based_api.v1 import (
    check_levels,
    register,
    render,
    startswith,
    Metric,
    OIDEnd,
    Result,
    Service,
    SNMPTree,
    State,
)

from .utils.temperature import (
    check_temperature,
)

_dell_os10_device_type = {
    "1": "Chassis",
    "2": "Stack",
    "3": "RPM",
    "4": "Supervisor",
    "5": "Linecard",
}

_dell_os10_oper_status = {
    "1": { "state": State.OK, "desc": "up" },
    "2": { "state": State.CRIT, "desc": "down" },
    "3": { "state": State.WARN, "desc": "testing" },
    "4": { "state": State.UNKNOWN, "desc": "unknown" },
    "5": { "state": State.WARN, "desc": "dormant" },
    "6": { "state": State.UNKNOWN, "desc": "not present" },
    "7": { "state": State.CRIT, "desc": "lower layer down" },
    "8": { "state": State.CRIT, "desc": "failed" },
}

from cmk.utils import debug
from pprint import pprint

#   .--chassis-------------------------------------------------------------.
#   |                        _                   _                         |
#   |                    ___| |__   __ _ ___ ___(_)___                     |
#   |                   / __| '_ \ / _` / __/ __| / __|                    |
#   |                  | (__| | | | (_| \__ \__ \ \__ \                    |
#   |                   \___|_| |_|\__,_|___/___/_|___/                    |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

def parse_dell_os10_chassis(string_table):
    section = {}

    os10_chassis_type = {
        "1": {"id": "s6000on", "desc": "Dell EMC Networking OS10 S6000-ON access switch"},
        "2": {"id": "s4048on", "desc": "Dell EMC Networking OS10 S4048-ON access switch"},
        "3": {"id": "s4048Ton", "desc": "Dell EMC Networking OS10 S4048T-ON access switch"},
        "4": {"id": "s3048on", "desc": "Dell EMC Networking OS10 S3048-ON access switch"},
        "5": {"id": "s6010on", "desc": "Dell EMC Networking OS10 S6010-ON access switch"},
        "6": {"id": "s4148Fon", "desc": "Dell EMC Networking OS10 S4148F-ON access switch"},
        "7": {"id": "s4128Fon", "desc": "Dell EMC Networking OS10 S4128F-ON access switch"},
        "8": {"id": "s4148Ton", "desc": "Dell EMC Networking OS10 S4148T-ON access switch"},
        "9": {"id": "s4128Ton", "desc": "Dell EMC Networking OS10 S4128T-ON access switch"},
        "10": {"id": "s4148FEon", "desc": "Dell EMC Networking OS10 S4148FE-ON access switch"},
        "11": {"id": "s4148Uon", "desc": "Dell EMC Networking OS10 S4148U-ON access switch"},
        "12": {"id": "s4200on", "desc": "Depreciated Dell EMC Networking OS10 S4200-ON access switch"},
        "13": {"id": "mx5108Non", "desc": "Dell EMC Networking OS10 MX5108N-ON access switch"},
        "14": {"id": "mx9116Non", "desc": "Dell EMC Networking OS10 MX9116N-ON access switch"},
        "15": {"id": "s5148Fon", "desc": "Dell EMC Networking OS10 S5148F-ON access switch"},
        "16": {"id": "z9100on", "desc": "Dell EMC Networking OS10 Z9100-ON access switch"},
        "17": {"id": "s4248FBon", "desc": "Dell EMC Networking OS10 S4248FB-ON access switch"},
        "18": {"id": "s4248FBLon", "desc": "Dell EMC Networking OS10 S4248FBL-ON access switch"},
        "19": {"id": "s4112Fon", "desc": "Dell EMC Networking OS10 S4112F-ON access switch"},
        "20": {"id": "s4112Ton", "desc": "Dell EMC Networking OS10 S4112T-ON access switch"},
        "21": {"id": "z9264Fon", "desc": "Dell EMC Networking OS10 Z9264F-ON access switch"},
        "22": {"id": "z9224Fon", "desc": "Dell EMC Networking OS10 Z9232F-ON access switch"},
        "23": {"id": "s5212Fon", "desc": "Dell EMC Networking OS10 S5212F-ON access switch"},
        "24": {"id": "s5224Fon", "desc": "Dell EMC Networking OS10 S5224F-ON access switch"},
        "25": {"id": "s5232Fon", "desc": "Dell EMC Networking OS10 S5232F-ON access switch"},
        "26": {"id": "s5248Fon", "desc": "Dell EMC Networking OS10 S5248F-ON access switch"},
        "27": {"id": "s5296Fon", "desc": "Dell EMC Networking OS10 S5296F-ON access switch"},
        "28": {"id": "z9332Fon", "desc": "Dell EMC Networking OS10 Z9332F-ON access switch"},
        "29": {"id": "n3248TEon", "desc": "Dell EMC Networking OS10 N3248TE-ON access switch"},
        "30": {"id": "z9432Fon", "desc": "Dell EMC Networking OS10 Z9432F-ON access switch"},
    }

    for line in string_table:
        section["Chassis " + line[0]] = {
            'type': os10_chassis_type.get(line[1], {"id": "unknown", "desc": "Unknown"}),
            'partnum': line[2],
            'servicetag': line[3],
            'temp': float(line[4]),
        }

    return section

def discover_dell_os10_chassis(section):
    for idx in section:
        yield Service(item=idx)

def check_dell_os10_chassis(item, params, section):
    if item in section:
        data = section[item]

        yield Result(state=State.OK,
                     summary=data['type']['desc'] + ", " + data['servicetag'])
        yield from check_temperature(data['temp'],
                                     params,
                                     unique_name="dell_os10_chassis_%s" % item)

register.snmp_section(
    name="dell_os10_chassis",
    parse_function=parse_dell_os10_chassis,
    fetch=SNMPTree(
            base=".1.3.6.1.4.1.674.11000.5000.100.4.1.1.3.1",
            oids=[ OIDEnd(), "2", "4", "7", "11" ],
    ),
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.674.11000.5000.100.2"),
)

register.check_plugin(
    name="dell_os10_chassis",
    sections=["dell_os10_chassis"],
    service_name="Dell OS10 %s",
    discovery_function=discover_dell_os10_chassis,
    check_function=check_dell_os10_chassis,
    check_default_parameters={},
    check_ruleset_name="temperature",
)

#   .--card----------------------------------------------------------------.
#   |                                           _                          |
#   |                          ___ __ _ _ __ __| |                         |
#   |                         / __/ _` | '__/ _` |                         |
#   |                        | (_| (_| | | | (_| |                         |
#   |                         \___\__,_|_|  \__,_|                         |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

def parse_dell_os10_card(string_table):
    section = {}

    os10_card_type = {
        "0": {"id": "notPresent", "desc": "not present"},
        "1": {"id": "s6000on", "desc": "S6000-ON 32 x 40Gbe QSFP+ Interface Module"},
        "2": {"id": "s4048on", "desc": "S4048-ON 48 x 10Gbe, 6 x 40Gbe QSFP+ Interface module"},
        "3": {"id": "s4048Ton", "desc": "S4048T-ON 48 x 10Gbe copper, 6 x 40Gbe QSFP+ Interface module"},
        "4": {"id": "s3048on", "desc": "S3048-ON 48 x 1Gbe copper, 4 x 10Gbe SFP+ Interface module"},
        "5": {"id": "s6010on", "desc": "S6010-ON 32 x 40Gbe QSFP+ Interface Module"},
        "6": {"id": "s4148Fon", "desc": "S4148F-ON 48 x 10Gbe, 2 x 40Gbe QSFP+, 4 x 100Gbe QSFP28 Interface module"},
        "7": {"id": "s4128Fon", "desc": "S4128F-ON 28 x 10Gbe, 2 x 100Gbe QSFP28 Interface module"},
        "8": {"id": "s4148Ton", "desc": "S4148T-ON 48 x 10Gbe copper, 2 x 40Gbe QSFP+, 4 x 100Gbe QSFP28 Interface module"},
        "9": {"id": "s4128Ton", "desc": "S4128T-ON 28 x 10Gbe copper, 2 x 100Gbe QSFP28 Interface module"},
        "10": {"id": "s4148FEon", "desc": "S4148FE-ON 48 x 10Gbe, 2 x 40Gbe QSFP+, 4 x 100Gbe QSFP28 Interface module"},
        "11": {"id": "s4148Uon", "desc": "S4148U-ON 24 x 8GFC/10Gbe 24 x 10Gbe, 2 x 40Gbe QSFP+, 4 x 100Gbe QSFP28 Interface module"},
        "12": {"id": "s4200on", "desc": "Deprecated: S4200-ON 40 x 10Gbe, 2 x 40Gbe QSFP+, 6 x 100Gbe QSFP28 Interface module"},
        "13": {"id": "mx5108Non", "desc": "MX5108N-ON 8 x 25Gbe server ports, 4x 10Gbe copper, 1 x 40Gbe QSFP+, 2 x 100Gbe QSFP28  Interface module"},
        "14": {"id": "mx9116Non", "desc": "MX9116N-ON  16 x 25Gbe server ports, 12 x 200Gbe DDQSFP, 4 x 100Gbe QSFP28 Interface module"},
        "15": {"id": "s5148Fon", "desc": "S5148F-ON 48x25GbE, 6x100GbE QSFP28 Interface Module"},
        "16": {"id": "z9100on", "desc": "Z9100-ON 32x100GbE QSFP28, 2x10GbE SFP+ Interface Module"},
        "17": {"id": "s4248FBon", "desc": "S4248FB-ON 40 x 10Gbe, 2 x 40Gbe QSFP+, 6 x 100Gbe QSFP28 Interface module"},
        "18": {"id": "s4248FBLon", "desc": "S4248FBL-ON 40 x 10Gbe, 2 x 40Gbe QSFP+, 6 x 100Gbe QSFP28 Interface module"},
        "19": {"id": "s4112Fon", "desc": "S4112F-ON Maverick 12x10GbE Base-T, 3x100GbE Interface Module"},
        "20": {"id": "s4112Ton", "desc": "S4112T-ON Maverick 12x10GbE, 3x100GbE Interface Module"},
        "21": {"id": "z9264Fon", "desc": "Z9264F-ON Tomahawk 2 64x100G, 2x10Gbe Interface Module"},
        "22": {"id": "z9232Fon", "desc": "Z9232F-ON 32x200GbE DD-QSFP28, 4x10GbE SFP+ Interface Module"},
        "23": {"id": "s5212Fon", "desc": "S5212F-ON 12x25GbE SFP28, 3x100GbE QSFP28 Interface Module"},
        "24": {"id": "s5224Fon", "desc": "S5224F-ON 24x25GbE SFP28, 4x100GbE QSFP28 Interface Module"},
        "25": {"id": "s5232Fon", "desc": "S5232F-ON 32x100GbE QSFP28, 2x10GbE SFP28 Interface Module"},
        "26": {"id": "s5248Fon", "desc": "S5248F-ON 48x100GbE SFP28, 4x100GbE QSFP28, 2x200GbE QSFP-DD Interface Module"},
        "27": {"id": "s5296Fon", "desc": "S5296F-ON 96x25GbE SFP28, 8x100GbE QSFP28 Interface Module"},
        "28": {"id": "z9332Fon", "desc": "Z9332F-ON Tomahawk 3 32x400G, 2x10Gbe Interface Module"},
        "29": {"id": "n3248TEon", "desc": "N3248TE-ON 48x1G, 4x10G, SFP+ Interface Module"},
        "30": {"id": "z9432Fon", "desc": "Z9432F-ON Trident 4 32x400G, 2x10Gbe Interface Module"},
    }

    os10_card_state = {
        "1": { "state": State.OK, "desc": "ready" }, 
        "2": { "state": State.WARN, "desc": "cardMisMatch" },
        "3": { "state": State.WARN, "desc": "cardProblem" },
        "4": { "state": State.WARN, "desc": "diagMode" },
        "5": { "state": State.CRIT, "desc": "cardAbsent" },
        "6": { "state": State.CRIT, "desc": "offline" },
    }

    for line in string_table:
        chassis, card = line[0].split('.')

        section["Chassis %s Card %s" % (chassis, card)] = {
            'type': os10_card_type.get(line[1], {"id": "unknown", "desc": "Unknown"}),
            'desc': line[2],
            'state': os10_card_state.get(line[3], { "state": State.UNKNOWN, "desc": "Unknown" }),
            'temp': float(line[4]),
            'servicetag': line[5],
        }

    return section

def discover_dell_os10_card(section):
    for idx in section:
        yield Service(item=idx)

def check_dell_os10_card(item, params, section):
    if item in section:
        data = section[item]

        yield Result(state=State.OK,
                     summary=data['type']['desc'] + ", " + data['servicetag'])
        yield Result(state=data["state"]["state"],
                     summary="State: %s" % data["state"]["desc"])
        yield from check_temperature(data['temp'],
                                     params,
                                     unique_name="dell_os10_card_%s" % item)

register.snmp_section(
    name="dell_os10_card",
    parse_function=parse_dell_os10_card,
    fetch=SNMPTree(
            base=".1.3.6.1.4.1.674.11000.5000.100.4.1.1.4.1",
            oids=[ OIDEnd(), "2", "3", "4", "5", "9" ],
    ),
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.674.11000.5000.100.2"),
)

register.check_plugin(
    name="dell_os10_card",
    sections=["dell_os10_card"],
    service_name="Dell OS10 %s",
    discovery_function=discover_dell_os10_card,
    check_function=check_dell_os10_card,
    check_default_parameters={},
    check_ruleset_name="temperature",
)

#   .--power supply--------------------------------------------------------.
#   |                                                         _            |
#   |    _ __   _____      _____ _ __   ___ _   _ _ __  _ __ | |_   _      |
#   |   | '_ \ / _ \ \ /\ / / _ \ '__| / __| | | | '_ \| '_ \| | | | |     |
#   |   | |_) | (_) \ V  V /  __/ |    \__ \ |_| | |_) | |_) | | |_| |     |
#   |   | .__/ \___/ \_/\_/ \___|_|    |___/\__,_| .__/| .__/|_|\__, |     |
#   |   |_|                                      |_|   |_|      |___/      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

def parse_dell_os10_powersupply(string_table):
    section = {}

    dell_os10_powersupply_type = {
        "1": "unknown",
        "2": "AC",
        "3": "DC",
    }

    for line in string_table:
        item = "%s %s Power Supply %s" % (_dell_os10_device_type.get(line[1], "Unknown"), line[2], line[0])
        section[item] = {
            "state": _dell_os10_oper_status.get(line[3], { "state": State.UNKNOWN, "desc": "unknown" }),
            "type": dell_os10_powersupply_type.get(line[4], "unknown"),
            "ppid": line[5],
        }
    
    return section

def discover_dell_os10_powersupply(section):
    for idx in section:
        yield Service(item=idx)

def check_dell_os10_powersupply(item, section):
    if item in section:
        data = section[item]

        yield Result(state=State.OK,
                     summary=data['type'] + ", " + data['ppid'])
        yield Result(state=data["state"]["state"],
                     summary="State: %s" % data["state"]["desc"])

register.snmp_section(
    name="dell_os10_powersupply",
    parse_function=parse_dell_os10_powersupply,
    fetch=SNMPTree(
            base=".1.3.6.1.4.1.674.11000.5000.100.4.1.2.1.1",
            oids=[ OIDEnd(), "2", "3", "4", "5", "6" ],
    ),
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.674.11000.5000.100.2.1"),
)

register.check_plugin(
    name="dell_os10_powersupply",
    sections=["dell_os10_powersupply"],
    service_name="Dell OS10 %s",
    discovery_function=discover_dell_os10_powersupply,
    check_function=check_dell_os10_powersupply,
)

#   .--fan tray------------------------------------------------------------.
#   |                 __               _                                   |
#   |                / _| __ _ _ __   | |_ _ __ __ _ _   _                 |
#   |               | |_ / _` | '_ \  | __| '__/ _` | | | |                |
#   |               |  _| (_| | | | | | |_| | | (_| | |_| |                |
#   |               |_|  \__,_|_| |_|  \__|_|  \__,_|\__, |                |
#   |                                                |___/                 |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

def parse_dell_os10_fantray(string_table):
    section = {}

    for line in string_table:
        item = "%s %s Fan Tray %s" % (_dell_os10_device_type.get(line[1], "Unknown"), line[2], line[0])
        section[item] = {
            "state": _dell_os10_oper_status.get(line[3], { "state": State.UNKNOWN, "desc": "unknown" }),
            "ppid": line[4],
        }
    
    return section

def discover_dell_os10_fantray(section):
    for idx in section:
        yield Service(item=idx)

def check_dell_os10_fantray(item, section):
    if item in section:
        data = section[item]

        yield Result(state=State.OK,
                     summary=data['ppid'])
        yield Result(state=data["state"]["state"],
                     summary="State: %s" % data["state"]["desc"])

register.snmp_section(
    name="dell_os10_fantray",
    parse_function=parse_dell_os10_fantray,
    fetch=SNMPTree(
            base=".1.3.6.1.4.1.674.11000.5000.100.4.1.2.2.1",
            oids=[ OIDEnd(), "2", "3", "4", "5" ],
    ),
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.674.11000.5000.100.2.1"),
)

register.check_plugin(
    name="dell_os10_fantray",
    sections=["dell_os10_fantray"],
    service_name="Dell OS10 %s",
    discovery_function=discover_dell_os10_fantray,
    check_function=check_dell_os10_fantray,
)

#   .--fan-----------------------------------------------------------------.
#   |                            __                                        |
#   |                           / _| __ _ _ __                             |
#   |                          | |_ / _` | '_ \                            |
#   |                          |  _| (_| | | | |                           |
#   |                          |_|  \__,_|_| |_|                           |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

def parse_dell_os10_fan(string_table):
    section = {}

    fan_entity = {
        "1": "Power Supply",
        "2": "Fan Tray",
    }

    for line in string_table:
        item = "%s %s %s %s Fan %s" % (_dell_os10_device_type.get(line[1], "Unknown"),
                                       line[2],
                                       fan_entity.get(line[3], "Unknown"),
                                       line[4],
                                       line[5])
        section[item] = {
            "state": _dell_os10_oper_status.get(line[6], { "state": State.UNKNOWN, "desc": "unknown" }),
            "id": line[0],
        }
    
    return section

def discover_dell_os10_fan(section):
    for idx in section:
        yield Service(item=idx)

def check_dell_os10_fan(item, section):
    if item in section:
        data = section[item]

        yield Result(state=data["state"]["state"],
                     summary="State: %s" % data["state"]["desc"])

register.snmp_section(
    name="dell_os10_fan",
    parse_function=parse_dell_os10_fan,
    fetch=SNMPTree(
            base=".1.3.6.1.4.1.674.11000.5000.100.4.1.2.3.1",
            oids=[ OIDEnd(), "2", "3", "4", "5", "6", "7" ],
    ),
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.674.11000.5000.100.2.1"),
)

register.check_plugin(
    name="dell_os10_fan",
    sections=["dell_os10_fan"],
    service_name="Dell OS10 %s",
    discovery_function=discover_dell_os10_fan,
    check_function=check_dell_os10_fan,
)
