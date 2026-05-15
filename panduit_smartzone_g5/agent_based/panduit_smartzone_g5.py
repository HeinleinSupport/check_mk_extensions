#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2. This file is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# tails. You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.


from collections.abc import Mapping # type: ignore
from dataclasses import dataclass # type: ignore
from typing import Any, List # type: ignore

from cmk.agent_based.v2 import (
    any_of,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    OIDEnd,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPSection,
    SNMPTree,
    startswith,
    State,
    StringTable,
)

from cmk.plugins.lib import (
    elphase,
    humidity,
    temperature,
)


#   .--Temperature---------------------------------------------------------.
#   |     _____                                   _                        |
#   |    |_   _|__ _ __ ___  _ __   ___ _ __ __ _| |_ _   _ _ __ ___       |
#   |      | |/ _ \ '_ ` _ \| '_ \ / _ \ '__/ _` | __| | | | '__/ _ \      |
#   |      | |  __/ | | | | | |_) |  __/ | | (_| | |_| |_| | | |  __/      |
#   |      |_|\___|_| |_| |_| .__/ \___|_|  \__,_|\__|\__,_|_|  \___|      |
#   |                       |_|                                            |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

@dataclass(frozen=True, kw_only=True)
class PanSZG5Temp:
    name: str
    status: int
    value: float
    unit: str
    th_status: tuple[State, str]
    th_lower: tuple[float, float]
    th_upper: tuple[float, float]

def parse_panduit_smartzone_g5_temp(string_table: StringTable) -> Mapping[str, PanSZG5Temp] | None:
    map_dev_status = {
        "1": (State.OK, "good"),
        "2": (State.WARN, "lower warning"),
        "3": (State.CRIT, "lower critical"),
        "4": (State.WARN, "upper warning"),
        "5": (State.CRIT, "upper critical"),
    }
    
    map_unit = {
        "1": "c",
        "2": "f",
    }
    
    unit = {}
    for pdu, scale in string_table[1]:
        unit[pdu] = map_unit.get(scale, "c")
        
    section = {}
    for id, name, status, value, th_status, th_lower_warn, th_lower_crit, th_upper_warn, th_upper_crit in string_table[0]:
        pdu = id.split(".")[0]
        section[id] = PanSZG5Temp(
            name=name,
            status=int(status),
            value=float(value),
            unit=unit.get(pdu, "c"),
            th_status=map_dev_status.get(th_status, (State.UNKNOWN, th_status)),
            th_lower=(float(th_lower_warn), float(th_lower_crit)),
            th_upper=(float(th_upper_warn), float(th_upper_crit)),
        )
    return section

snmp_section_panduit_smartzone_g5_temp = SNMPSection(
    name="panduit_smartzone_g5_temp",
    parse_function=parse_panduit_smartzone_g5_temp,
    detect=any_of(
        startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.19536.10.1"),
    ),
    fetch=[
        SNMPTree(
            base = ".1.3.6.1.4.1.19536.10.1.4.2.1",
            oids = [
                OIDEnd(),
                "2",  # pdug5TemperatureName
                "3",  # pdug5TemperatureProbeStatus
                "4",  # pdug5TemperatureValue
                "5",  # pdug5TemperatureThStatus
                "6",  # pdug5TemperatureThLowerWarning
                "7",  # pdug5TemperatureThLowerCritical
                "8",  # pdug5TemperatureThUpperWarning
                "9",  # pdug5TemperatureThUpperCritical
        ]),
        SNMPTree(
            base=".1.3.6.1.4.1.19536.10.1.4.1.1",
            oids=[
                OIDEnd(),
                "1",  # pdug5TemperatureScale
            ]
        )
    ],
)

def discover_panduit_smartzone_g5_temp(section: Mapping[str, PanSZG5Temp]) -> DiscoveryResult:
    for id, data in section.items():
        if data.status > 1:
            yield Service(item=id)
            
def check_panduit_smartzone_g5_temp(item, params, section: Mapping[str, PanSZG5Temp]) -> CheckResult:
    if item in section:
        data = section[item]
        yield Result(
            state=State.OK,
            summary=data.name,
        )
        if data.status > 1:
            yield from temperature.check_temperature(
                reading=data.value,
                params=params,
                dev_unit=data.unit,
                dev_status=data.th_status[0].value,
                dev_status_name=data.th_status[1],
                dev_levels=data.th_upper,
                dev_levels_lower=data.th_lower,
            )
        else:
            yield Result(
                state=State.CRIT,
                summary="Sensor disconnected",
            )
            
check_plugin_panduit_smartzone_g5_temp = CheckPlugin(
    name="panduit_smartzone_g5_temp",
    sections=["panduit_smartzone_g5_temp"],
    service_name="Temperature PDU %s",
    discovery_function=discover_panduit_smartzone_g5_temp,
    check_function=check_panduit_smartzone_g5_temp,
    check_default_parameters={},
    check_ruleset_name="temperature",
)


#   .--Humidity------------------------------------------------------------.
#   |              _   _                 _     _ _ _                       |
#   |             | | | |_   _ _ __ ___ (_) __| (_) |_ _   _               |
#   |             | |_| | | | | '_ ` _ \| |/ _` | | __| | | |              |
#   |             |  _  | |_| | | | | | | | (_| | | |_| |_| |              |
#   |             |_| |_|\__,_|_| |_| |_|_|\__,_|_|\__|\__, |              |
#   |                                                  |___/               |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

@dataclass(frozen=True, kw_only=True)
class PanSZG5Humidity:
    name: str
    status: int
    value: float
    th_status: tuple[State, str]
    th_lower: tuple[float, float]
    th_upper: tuple[float, float]

def parse_panduit_smartzone_g5_humidity(info: StringTable) -> Mapping[str, PanSZG5Humidity]:
    map_dev_status = {
        "1": (State.OK, "good"),
        "2": (State.WARN, "lower warning"),
        "3": (State.CRIT, "lower critical"),
        "4": (State.WARN, "upper warning"),
        "5": (State.CRIT, "upper critical"),
    }
    
    section = {}
    for id, name, status, value, th_status, th_lower_warn, th_lower_crit, th_upper_warn, th_upper_crit in info:
        section[id] = PanSZG5Humidity(
            name=name,
            status=int(status),
            value=float(value),
            th_status=map_dev_status.get(th_status, (State.UNKNOWN, th_status)),
            th_lower=(float(th_lower_warn), float(th_lower_crit)),
            th_upper=(float(th_upper_warn), float(th_upper_crit)),
        )
    return section

snmp_section_panduit_smartzone_g5_humidity = SimpleSNMPSection(
    name="panduit_smartzone_g5_humidity",
    parse_function=parse_panduit_smartzone_g5_humidity,
    detect=any_of(
        startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.19536.10.1"),
    ),
    fetch=SNMPTree(
        base = ".1.3.6.1.4.1.19536.10.1.4.3.1",
        oids = [
            OIDEnd(),
            "2",  # pdug5HumidityName
            "3",  # pdug5HumidityProbeStatus
            "4",  # pdug5HumidityValue
            "5",  # pdug5HumidityThStatus
            "6",  # pdug5HumidityThLowerWarning
            "7",  # pdug5HumidityThLowerCritical
            "8",  # pdug5HumidityThUpperWarning
            "9",  # pdug5HumidityThUpperCritical
    ]),
)

def discover_panduit_smartzone_g5_humidity(section: Mapping[str, PanSZG5Humidity]) -> DiscoveryResult:
    for id, data in section.items():
        if data.status > 1:
            yield Service(item=id)
            
def check_panduit_smartzone_g5_humidity(item, params, section: Mapping[str, PanSZG5Humidity]) -> CheckResult:
    if item in section:
        data = section[item]
        yield Result(
            state=State.OK,
            summary=data.name,
        )
        if data.status > 1:
            levels_upper, levels_lower = None, None
            if isinstance(params, (dict, Mapping)):
                levels_upper = params.get("levels") or data.th_upper
                levels_lower = params.get("levels_lower") or data.th_lower
            
            tmp_params = {
                "levels": levels_upper,
                "levels_lower": levels_lower,
            }

            yield from humidity.check_humidity(
                humidity=data.value,
                params=tmp_params,
            )
            yield Result(
                state=data.th_status[0],
                summary="State on device: " + data.th_status[1],
            )
        else:
            yield Result(
                state=State.CRIT,
                summary="Sensor disconnected",
            )
            
check_plugin_panduit_smartzone_g5_humidity = CheckPlugin(
    name="panduit_smartzone_g5_humidity",
    sections=["panduit_smartzone_g5_humidity"],
    service_name="Humidity PDU %s",
    discovery_function=discover_panduit_smartzone_g5_humidity,
    check_function=check_panduit_smartzone_g5_humidity,
    check_default_parameters={},
    check_ruleset_name="humidity",
)


#   .--Door----------------------------------------------------------------.
#   |                       ____                                           |
#   |                      |  _ \  ___   ___  _ __                         |
#   |                      | | | |/ _ \ / _ \| '__|                        |
#   |                      | |_| | (_) | (_) | |                           |
#   |                      |____/ \___/ \___/|_|                           |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

# @dataclass(frozen=True, kw_only=True)
# class PanSZG5Door:
#     name: str
#     status: int
#     value: tuple[State, str]

# def parse_panduit_smartzone_g5_door(info: StringTable) -> Mapping[str, PanSZG5Door]:
#     map_door_status = {
#         "1": (State.WARN, "Door open"),
#         "2": (State.OK, "Door closed"),
#         "3": (State.CRIT, "Bad door sensor"),
#     }
    
#     section = {}
#     for id, name, status, door_status in info:
#         section[id] = PanSZG5Door(
#             name=name,
#             status=int(status),
#             value=map_door_status.get(door_status, (State.UNKNOWN, door_status)),
#         )
#     return section

# snmp_section_panduit_smartzone_g5_door = SimpleSNMPSection(
#     name="panduit_smartzone_g5_door",
#     parse_function=parse_panduit_smartzone_g5_door,
#     detect=any_of(
#         startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.19536.10.1"),
#     ),
#     fetch=SNMPTree(
#         base = ".1.3.6.1.4.1.19536.10.1.4.4.1",
#         oids = [
#             OIDEnd(),
#             "2",  # pdug5DoorName
#             "3",  # pdug5DoorProbeStatus
#             "4",  # pdug5DoorState
#     ]),
# )

# def discover_panduit_smartzone_g5_door(section: Mapping[str, PanSZG5Door]) -> DiscoveryResult:
#     for id, data in section.items():
#         if data.status > 1:
#             yield Service(item=id)
            
# def check_panduit_smartzone_g5_door(item, params, section: Mapping[str, PanSZG5Door]) -> CheckResult:
#     if debug.enabled():
#         pprint(params)
#     if item in section:
#         data = section[item]
#         yield Result(
#             state=State.OK,
#             summary=data.name,
#         )
#         if data.status > 1:
#             levels_upper, levels_lower = None, None
#             if isinstance(params, (dict, Mapping)):
#                 levels_upper = params.get("levels") or data.th_upper
#                 levels_lower = params.get("levels_lower") or data.th_lower
            
#             tmp_params = {
#                 "levels": levels_upper,
#                 "levels_lower": levels_lower,
#             }

#             yield from temperature.check_temperature(
#                 temperature=data.value,
#                 params=tmp_params,
#             )
#             yield Result(
#                 state=data.th_status[0],
#                 summary="State on device: " + data.th_status[1],
#             )
#         else:
#             yield Result(
#                 state=State.CRIT,
#                 summary="Sensor disconnected",
#             )
            
# check_plugin_panduit_smartzone_g5_door = CheckPlugin(
#     name="panduit_smartzone_g5_door",
#     sections=["panduit_smartzone_g5_door"],
#     service_name="door PDU %s",
#     discovery_function=discover_panduit_smartzone_g5_door,
#     check_function=check_panduit_smartzone_g5_door,
#     check_default_parameters={},
#     check_ruleset_name="door",
# )


#   .--InputPhase----------------------------------------------------------.
#   |        ___                   _   ____  _                             |
#   |       |_ _|_ __  _ __  _   _| |_|  _ \| |__   __ _ ___  ___          |
#   |        | || '_ \| '_ \| | | | __| |_) | '_ \ / _` / __|/ _ \         |
#   |        | || | | | |_) | |_| | |_|  __/| | | | (_| \__ \  __/         |
#   |       |___|_| |_| .__/ \__,_|\__|_|   |_| |_|\__,_|___/\___|         |
#   |                 |_|                                                  |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

def parse_panduit_smartzone_g5_input(info: StringTable):
    map_dev_status = {
        "1": (State.OK, "good"),
        "2": (State.WARN, "lower warning"),
        "3": (State.CRIT, "lower critical"),
        "4": (State.WARN, "upper warning"),
        "5": (State.CRIT, "upper critical"),
    }
    
    map_quantity = {
        "voltage": {
            "value": 2,
            "factor": 0.1,
            "status": 3,
            "lower_warn": 4,
            "lower_crit": 5,
            "upper_warn": 6,
            "upper_crit": 7,
        },
        "current": {
            "value": 10,
            "factor": 0.01,
            "status": 3,
            "lower_warn": 4,
            "lower_crit": 5,
            "upper_warn": 6,
            "upper_crit": 7,
        },
        "appower": {
            "value": 18,
            "factor": 1.0,
        },
        "power": {
            "value": 19,
            "factor": 1.0,
        },
        "energy": {
            "value": 20,
            "factor": 1.0,
        },
    }
    
    section = {}
    for line in info:
        section[line[0]] = {}
        for quantity, data in map_quantity.items():
            value = float(line[data["value"]]) * data["factor"]
            section[line[0]][quantity] = value
            if "status" in data:
                dev_status = map_dev_status.get(line[data["status"]],
                                                (State.UNKNOWN, line[data["status"]]))
                if dev_status[0] != State.OK:
                    section[line[0]][quantity] = (
                        value,
                        (dev_status[0], dev_status[1])
                    )
    return section

snmp_section_panduit_smartzone_g5_input = SimpleSNMPSection(
    name="panduit_smartzone_g5_input",
    parse_function=parse_panduit_smartzone_g5_input,
    detect=any_of(
        startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.19536.10.1"),
    ),
    fetch=SNMPTree(
        base = ".1.3.6.1.4.1.19536.10.1.2.2.1",
        oids = [
            OIDEnd(),
            "2",  # pdug5InputPhaseVoltageMeasType
            "3",  # pdug5InputPhaseVoltage
            "4",  # pdug5InputPhaseVoltageThStatus
            "5",  # pdug5InputPhaseVoltageThLowerWarning
            "6",  # pdug5InputPhaseVoltageThLowerCritical
            "7",  # pdug5InputPhaseVoltageThUpperWarning
            "8",  # pdug5InputPhaseVoltageThUpperCritical
            "9",  # pdug5InputPhaseCurrentMeasType
            "10", # pdug5InputPhaseCurrentRating
            "11", # pdug5InputPhaseCurrent
            "12", # pdug5InputPhaseCurrentThStatus
            "13", # pdug5InputPhaseCurrentThLowerWarning
            "14", # pdug5InputPhaseCurrentThLowerCritical
            "15", # pdug5InputPhaseCurrentThUpperWarning
            "16", # pdug5InputPhaseCurrentThUpperCritical
            "17", # pdug5InputPhaseCurrentPercentLoad
            "18", # pdug5InputPhasePowerMeasType
            "19", # pdug5InputPhasePowerVA
            "20", # pdug5InputPhasePowerWatts
            "21", # pdug5InputPhasePowerWattHour
            "23", # pdug5InputPhasePowerFactor
            "24", # pdug5InputPhasePowerVAR
    ]),
)

def discover_panduit_smartzone_g5_input(section) -> DiscoveryResult:
    for id, data in section.items():
        yield Service(item=id)

def check_panduit_smartzone_g5_input(item, params, section) -> CheckResult:
    if item in section:
        yield from elphase.check_elphase(params, elphase.ElPhase.from_dict(section[item]))
            
check_plugin_panduit_smartzone_g5_input = CheckPlugin(
    name="panduit_smartzone_g5_input",
    sections=["panduit_smartzone_g5_input"],
    service_name="Phase Input %s",
    discovery_function=discover_panduit_smartzone_g5_input,
    check_function=check_panduit_smartzone_g5_input,
    check_default_parameters={},
    check_ruleset_name="el_inphase",
)


#   .--GroupOutput---------------------------------------------------------.
#   |      ____                        ___        _               _        |
#   |     / ___|_ __ ___  _   _ _ __  / _ \ _   _| |_ _ __  _   _| |_      |
#   |    | |  _| '__/ _ \| | | | '_ \| | | | | | | __| '_ \| | | | __|     |
#   |    | |_| | | | (_) | |_| | |_) | |_| | |_| | |_| |_) | |_| | |_      |
#   |     \____|_|  \___/ \__,_| .__/ \___/ \__,_|\__| .__/ \__,_|\__|     |
#   |                          |_|                   |_|                   |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

def parse_panduit_smartzone_g5_output(info: StringTable):
    map_dev_status = {
        "1": (State.OK, "good"),
        "2": (State.WARN, "lower warning"),
        "3": (State.CRIT, "lower critical"),
        "4": (State.WARN, "upper warning"),
        "5": (State.CRIT, "upper critical"),
    }
    
    map_quantity = {
        "voltage": {
            "value": 3,
            "factor": 0.1,
            "status": 4,
        },
        "current": {
            "value": 5,
            "factor": 0.01,
            "status": 6,
        },
    }

    section = {}
    for line in info:
        section[line[0]] = {
            "x-name": line[1][:-1],
            "x-type": int(line[2]),
            "x-count": int(line[11]),
            "x-breakerstatus": int(line[12]),
            "output_load": float(line[7]),
            "appower": float(line[8]),
            "power": float(line[9]),
            "energy": float(line[10]),
        }
        for quantity, config in map_quantity.items():
            value = float(line[config["value"]]) * config["factor"]
            section[line[0]][quantity] = value
            if "status" in config:
                dev_status = map_dev_status.get(line[config["status"]],
                                                (State.UNKNOWN, line[config["status"]]))
                if dev_status[0] != State.OK:
                    section[line[0]][quantity] = (
                        value,
                        (dev_status[0], dev_status[1])
                    )
    return section

snmp_section_panduit_smartzone_g5_output = SimpleSNMPSection(
    name="panduit_smartzone_g5_output",
    parse_function=parse_panduit_smartzone_g5_output,
    detect=any_of(
        startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.19536.10.1"),
    ),
    fetch=SNMPTree(
        base = ".1.3.6.1.4.1.19536.10.1.3.1.1",
        oids = [
            OIDEnd(),
            "2",  # pdug5GroupName
            "3",  # pdug5GroupType
            "5",  # pdug5GroupVoltage
            "6",  # pdug5GroupVoltageThStatus
            "12", # pdug5GroupCurrent
            "13", # pdug5GroupCurrentThStatus
            "18", # pdug5GroupCurrentPercentLoad
            "19", # pdug5GroupPowerVA
            "20", # pdug5GroupPowerWatts
            "21", # pdug5GroupPowerWattHour
            "25", # pdug5GroupOutletCount
            "26", # pdug5GroupBreakerStatus
    ]),
)

def discover_panduit_smartzone_g5_output(section) -> DiscoveryResult:
    for id, data in section.items():
        if data["x-type"] > 0:
            yield Service(item=id)

def check_panduit_smartzone_g5_output(item: str, params, section) -> CheckResult:
    if item in section:
        data = section[item]
        yield Result(
            state=State.OK,
            summary=data["x-name"],
        )
        if data["x-breakerstatus"] == 3:
            yield Result(
                state=State.CRIT,
                summary="Breaker is off",
            )
        yield from elphase.check_elphase(params, elphase.ElPhase.from_dict(section[item]))
            
check_plugin_panduit_smartzone_g5_output = CheckPlugin(
    name="panduit_smartzone_g5_output",
    sections=["panduit_smartzone_g5_output"],
    service_name="Phase Output %s",
    discovery_function=discover_panduit_smartzone_g5_output,
    check_function=check_panduit_smartzone_g5_output,
    check_default_parameters={},
    check_ruleset_name="ups_outphase",
)


#   .--Outlet--------------------------------------------------------------.
#   |                      ___        _   _      _                         |
#   |                     / _ \ _   _| |_| | ___| |_                       |
#   |                    | | | | | | | __| |/ _ \ __|                      |
#   |                    | |_| | |_| | |_| |  __/ |_                       |
#   |                     \___/ \__,_|\__|_|\___|\__|                      |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

def parse_panduit_smartzone_g5_outlet(info: StringTable):
    map_dev_status = {
        "1": (State.OK, "good"),
        "2": (State.WARN, "lower warning"),
        "3": (State.CRIT, "lower critical"),
        "4": (State.WARN, "upper warning"),
        "5": (State.CRIT, "upper critical"),
    }
    
    map_quantity = {
        "current": {
            "value": 3,
            "factor": 0.01,
            "status": 4,
        },
    }
    
    map_type = {
        "1": "iecC13",
        "2": "iecC19",
        "3": "nema5-20R",
        "4": "iecC13iecC15combo",
        "5": "iecC13iecC15iec19combo",
        "10": "uk",
        "11": "french",
        "12": "schuko",
        "20": "nema515",
        "21": "nema51520",
        "22": "nema520",
        "23": "nemaL520",
        "24": "nemaL530",
        "25": "nema615",
        "26": "nema620",
        "27": "nemaL620",
        "28": "nemaL630",
        "29": "nemaL715",
        "30": "rf203p277",
    }

    section = {}
    for line in info:
        if line[1] != '\x00' and int(line[2]) > 0:
            section[line[0]] = {
                "x-name": line[1],
                "x-description": map_type.get(line[2], "unknown ("+line[2]+")"),
                "output_load": float(line[5]),
                "appower": float(line[6]),
                "power": float(line[7]),
                "energy": float(line[8]),
            }
            for quantity, config in map_quantity.items():
                value = float(line[config["value"]]) * config["factor"]
                section[line[0]][quantity] = value
                if "status" in config:
                    dev_status = map_dev_status.get(line[config["status"]],
                                                    (State.UNKNOWN, line[config["status"]]))
                    if dev_status[0] != State.OK:
                        section[line[0]][quantity] = (
                            value,
                            (dev_status[0], dev_status[1])
                        )
    return section

snmp_section_panduit_smartzone_g5_outlet = SimpleSNMPSection(
    name="panduit_smartzone_g5_outlet",
    parse_function=parse_panduit_smartzone_g5_outlet,
    detect=any_of(
        startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.19536.10.1"),
    ),
    fetch=SNMPTree(
        base = ".1.3.6.1.4.1.19536.10.1.5.1.1",
        oids = [
            OIDEnd(),
            "2",  # pdug5OutletName
            "3",  # pdug5OutletType
            "5",  # pdug5OutletCurrent
            "6",  # pdug5OutletActivePowerThStatus
            "11", # pdug5OutletCurrentPercentLoad
            "12", # pdug5OutletVA
            "13", # pdug5OutletWatts
            "14", # pdug5OutletWh
    ]),
)

def discover_panduit_smartzone_g5_outlet(section) -> DiscoveryResult:
    for id, data in section.items():
        yield Service(item=id)

def check_panduit_smartzone_g5_outlet(item: str, params, section) -> CheckResult:
    if item in section:
        data = section[item]
        yield Result(
            state=State.OK,
            summary=data["x-name"],
        )
        yield Result(
            state=State.OK,
            summary=data["x-description"],
        )
        yield from elphase.check_elphase(params, elphase.ElPhase.from_dict(section[item]))

check_plugin_panduit_smartzone_g5_outlet = CheckPlugin(
    name="panduit_smartzone_g5_outlet",
    sections=["panduit_smartzone_g5_outlet"],
    service_name="Outlet %s",
    discovery_function=discover_panduit_smartzone_g5_outlet,
    check_function=check_panduit_smartzone_g5_outlet,
    check_default_parameters={},
    check_ruleset_name="ups_outphase",
)
