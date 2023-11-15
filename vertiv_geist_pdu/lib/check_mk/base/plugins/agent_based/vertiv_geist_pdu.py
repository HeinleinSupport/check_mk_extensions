#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2023 Heinlein Support GmbH
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
    any_of,
    contains,
    register,
    Result,
    Service,
    SNMPTree,
    State,
)

from .agent_based_api.v1.type_defs import (
    CheckResult,
    DiscoveryResult,
)

from .utils.elphase import check_elphase
from .utils.temperature import check_temperature
from .utils.humidity import check_humidity

def parse_vertiv_geist_pdu(string_table):
    section = {
        'thd': {'temp': {}, 'hum': {}, 'dew': {} },
        'a2d': {},
        'main': {},
        'phase': {},
    }

    # Temperature, Humidity and Dewpoint sensors
    for label, avail, temp, hum, dew in string_table[0]:
        if avail == "1":
            section['thd']['temp'][label] = int(temp) / 10.0
            section['thd']['hum'][label] = int(hum)
            section['thd']['dew'][label] = int(dew) / 10.0

    # analog sensors
    for label, avail, value, display, mode, units, min, max, lowlabel, highlabel, analoglabel in string_table[1]:
        if avail == "1":
            section['a2d'][label] = {
                'value': int(value),
                'display': display,
                'mode': int(mode),
                'units': units,
                'min': int(min),
                'max': int(max),
                'label_low': lowlabel,
                'label_high': highlabel,
                'label_analog': analoglabel,
            }

    # PDU main table
    for mainserial, mainname, mainlabel, avail, metertype, totalname, totallabel, realpower, apparentpower, powerfactor, energy in string_table[2]:
        if avail == "1":
            section['main'][totallabel] = {
                'serial': mainserial,
                'type': mainname,
                'name': mainlabel,
                'metertype': int(metertype),
                'totalname': totalname,
                'power': int(realpower),
                'appower': int(apparentpower),
                'output_load': int(powerfactor),
                'energy': int(energy),
            }

    # PDU phase table
    for name, label, voltage, current, realpower, appower, load, energy in string_table[3]:
        section['phase'][label] = {
            'name': name,
            'voltage': int(voltage) / 10.0,
            'current': int(current) / 100.0,
            'power': int(realpower),
            'appower': int(appower),
            'output_load': int(load),
            'energy': int(energy),
        }
            
    return section

register.snmp_section(
    name="vertiv_geist_pdu",
    parse_function=parse_vertiv_geist_pdu,
    fetch=[
        SNMPTree(
            base=".1.3.6.1.4.1.21239.5.2.9.1",
            oids=[
                # "2", # VERTIV-V5-MIB::thdSensorSerial
                "3", # VERTIV-V5-MIB::thdSensorLabel
                "4", # VERTIV-V5-MIB::thdSensorAvail
                "5", # VERTIV-V5-MIB::thdSensorTemp
                "6", # VERTIV-V5-MIB::thdSensorHumidity
                "7", # VERTIV-V5-MIB::thdSensorDewPoint
            ]),
        SNMPTree(
            base=".1.3.6.1.4.1.21239.5.2.11.1",
            oids=[
                # "2",  # VERTIV-V5-MIB::a2dSensorSerial
                "3",  # VERTIV-V5-MIB::a2dSensorLabel
                "4",  # VERTIV-V5-MIB::a2dSensorAvail
                "5",  # VERTIV-V5-MIB::a2dSensorValue
                "6",  # VERTIV-V5-MIB::a2dSensorDisplayValue
                "7",  # VERTIV-V5-MIB::a2dSensorMode
                "8",  # VERTIV-V5-MIB::a2dSensorUnits
                "9",  # VERTIV-V5-MIB::a2dSensorMin
                "10", # VERTIV-V5-MIB::a2dSensorMax
                "11", # VERTIV-V5-MIB::a2dSensorLowLabel
                "12", # VERTIV-V5-MIB::a2dSensorHighLabel
                "13", # VERTIV-V5-MIB::a2dSensorAnalogLabel
            ]),
        SNMPTree(
            base=".1.3.6.1.4.1.21239.5.2.3.1.1",
            oids=[
                "2",  # VERTIV-V5-MIB::pduMainSerial
                "3",  # VERTIV-V5-MIB::pduMainName
                "4",  # VERTIV-V5-MIB::pduMainLabel
                "5",  # VERTIV-V5-MIB::pduMainAvail
                "6",  # VERTIV-V5-MIB::pduMeterType
                "7",  # VERTIV-V5-MIB::pduTotalName
                "8",  # VERTIV-V5-MIB::pduTotalLabel
                "9",  # VERTIV-V5-MIB::pduTotalRealPower
                "10", # VERTIV-V5-MIB::pduTotalApparentPower
                "11", # VERTIV-V5-MIB::pduTotalPowerFactor
                "12", # VERTIV-V5-MIB::pduTotalEnergy
            ]),
        SNMPTree(
            base=".1.3.6.1.4.1.21239.5.2.3.2.1",
            oids=[
                "2",  # VERTIV-V5-MIB::pduPhaseName
                "3",  # VERTIV-V5-MIB::pduPhaseLabel
                "4",  # VERTIV-V5-MIB::pduPhaseVoltage
                "8",  # VERTIV-V5-MIB::pduPhaseCurrent
                "12", # VERTIV-V5-MIB::pduPhaseRealPower
                "13", # VERTIV-V5-MIB::pduPhaseApparentPower
                "14", # VERTIV-V5-MIB::pduPhasePowerFactor
                "15", # VERTIV-V5-MIB::pduPhaseEnergy
            ]),
        ],
    detect=any_of(
        contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.21239.42.1.53"),  # IMD3 unit
    ),
)

def discover_vertiv_geist_pdu_thd(section, params, sfunc) -> DiscoveryResult:
    for sensorlabel, sensordata in section['thd'][sfunc].items():
        yield Service(
            item=sensorlabel,
            parameters=params,
        )

#   .--temperature---------------------------------------------------------.
#   |      _                                      _                        |
#   |     | |_ ___ _ __ ___  _ __   ___ _ __ __ _| |_ _   _ _ __ ___       |
#   |     | __/ _ \ '_ ` _ \| '_ \ / _ \ '__/ _` | __| | | | '__/ _ \      |
#   |     | ||  __/ | | | | | |_) |  __/ | | (_| | |_| |_| | | |  __/      |
#   |      \__\___|_| |_| |_| .__/ \___|_|  \__,_|\__|\__,_|_|  \___|      |
#   |                       |_|                                            |
#   +----------------------------------------------------------------------+
#   |                            main check                                |
#   '----------------------------------------------------------------------'

def check_vertiv_geist_pdu_thd_temp(item, params, section) -> CheckResult:
    if item in section['thd']['temp']:
        sensordata = section['thd']['temp'][item]
        yield from check_temperature(sensordata,
                                     params,
        )

register.check_plugin(
    name="vertiv_geist_pdu_thd_temp",
    sections=['vertiv_geist_pdu'],
    service_name="Temperature %s",
    discovery_function=lambda section: (yield from discover_vertiv_geist_pdu_thd(
        section,
        {},
        'temp'
    )),
    check_function=check_vertiv_geist_pdu_thd_temp,
    check_ruleset_name='temperature',
    check_default_parameters={},
)

#.
#   .--humidity------------------------------------------------------------.
#   |              _                     _     _ _ _                       |
#   |             | |__  _   _ _ __ ___ (_) __| (_) |_ _   _               |
#   |             | '_ \| | | | '_ ` _ \| |/ _` | | __| | | |              |
#   |             | | | | |_| | | | | | | | (_| | | |_| |_| |              |
#   |             |_| |_|\__,_|_| |_| |_|_|\__,_|_|\__|\__, |              |
#   |                                                  |___/               |
#   +----------------------------------------------------------------------+


def check_vertiv_geist_pdu_thd_hum(item, params, section) -> CheckResult:
    if item in section['thd']['hum']:
        sensordata = section['thd']['hum'][item]
        yield from check_humidity(
            sensordata,
            params
        )

register.check_plugin(
    name="vertiv_geist_pdu_thd_hum",
    sections=['vertiv_geist_pdu'],
    service_name="Humidity %s",
    discovery_function=lambda section: (yield from discover_vertiv_geist_pdu_thd(
        section,
        {},
        'hum'
    )),
    check_function=check_vertiv_geist_pdu_thd_hum,
    check_ruleset_name='humidity',
    check_default_parameters={},
)

#   .--Dew Point-----------------------------------------------------------.
#   |            ____                  ____       _       _                |
#   |           |  _ \  _____      __ |  _ \ ___ (_)_ __ | |_              |
#   |           | | | |/ _ \ \ /\ / / | |_) / _ \| | '_ \| __|             |
#   |           | |_| |  __/\ V  V /  |  __/ (_) | | | | | |_              |
#   |           |____/ \___| \_/\_/   |_|   \___/|_|_| |_|\__|             |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

def check_vertiv_geist_pdu_thd_dew(item, params, section) -> CheckResult:
    if item in section['thd']['dew']:
        sensordata = section['thd']['dew'][item]
        yield from check_temperature(sensordata,
                                     params,
                                     )

register.check_plugin(
    name="vertiv_geist_pdu_thd_dewpoint",
    sections=['vertiv_geist_pdu'],
    service_name="Dewpoint %s",
    discovery_function=lambda section: (yield from discover_vertiv_geist_pdu_thd(
        section,
        {},
        'dew'
    )),
    check_function=check_vertiv_geist_pdu_thd_dew,
    check_ruleset_name='temperature',
    check_default_parameters={},
)

#   .--A2D Sensors---------------------------------------------------------.
#   |         _    ____  ____    ____                                      |
#   |        / \  |___ \|  _ \  / ___|  ___ _ __  ___  ___  _ __ ___       |
#   |       / _ \   __) | | | | \___ \ / _ \ '_ \/ __|/ _ \| '__/ __|      |
#   |      / ___ \ / __/| |_| |  ___) |  __/ | | \__ \ (_) | |  \__ \      |
#   |     /_/   \_\_____|____/  |____/ \___|_| |_|___/\___/|_|  |___/      |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

def discover_vertiv_geist_pdu_a2d(section, mode) -> DiscoveryResult:
    for sensorlabel, sensordata in section['a2d'].items():
        if sensordata['mode'] == mode:
            yield Service(item=sensorlabel)

def check_vertiv_geist_pdu_a2d_door(item, params, section) -> CheckResult:
    if item in section['a2d']:
        data = section['a2d'][item]
        if data['value'] == params['ok']:
            yield Result(state=State.OK, summary="%d: %s" % (data['value'], data['display']))
        else:
            yield Result(state=State.CRIT, summary="%d: %s" % (data['value'], data['label_analog']))

register.check_plugin(
    name="vertiv_geist_pdu_a2d_door",
    sections=['vertiv_geist_pdu'],
    service_name="A2D Door %s",
    discovery_function=lambda section: (yield from discover_vertiv_geist_pdu_a2d(section, 1)),
    check_function=check_vertiv_geist_pdu_a2d_door,
    check_ruleset_name='vertiv_geist_pdu_a2d_binary',
    check_default_parameters={'ok': 0},
)

#   .--PDU Main Table------------------------------------------------------.
#   |  ____  ____  _   _   __  __       _         _____     _     _        |
#   | |  _ \|  _ \| | | | |  \/  | __ _(_)_ __   |_   _|_ _| |__ | | ___   |
#   | | |_) | | | | | | | | |\/| |/ _` | | '_ \    | |/ _` | '_ \| |/ _ \  |
#   | |  __/| |_| | |_| | | |  | | (_| | | | | |   | | (_| | |_) | |  __/  |
#   | |_|   |____/ \___/  |_|  |_|\__,_|_|_| |_|   |_|\__,_|_.__/|_|\___|  |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

def discover_vertiv_geist_pdu_main(section) -> DiscoveryResult:
    for sensorlabel, sensordata in section['main'].items():
        yield Service(item=sensorlabel)

def check_vertiv_geist_pdu_main(item, params, section) -> CheckResult:
    if item in section['main']:
        data = section['main'][item]
        yield Result(
            state=State.OK,
            summary="Serial: %s" % data['serial']
        )
        yield from check_elphase(item, params, section['main'])

register.check_plugin(
    name="vertiv_geist_pdu_pdu_main",
    sections=['vertiv_geist_pdu'],
    service_name="PDU Main %s",
    discovery_function=discover_vertiv_geist_pdu_main,
    check_function=check_vertiv_geist_pdu_main,
    check_ruleset_name='ups_outphase',
    check_default_parameters={},
)

#   .--PDU Phase Table-----------------------------------------------------.
#   |           ____  ____  _   _   ____  _                                |
#   |          |  _ \|  _ \| | | | |  _ \| |__   __ _ ___  ___             |
#   |          | |_) | | | | | | | | |_) | '_ \ / _` / __|/ _ \            |
#   |          |  __/| |_| | |_| | |  __/| | | | (_| \__ \  __/            |
#   |          |_|   |____/ \___/  |_|   |_| |_|\__,_|___/\___|            |
#   |                                                                      |
#   |                       _____     _     _                              |
#   |                      |_   _|_ _| |__ | | ___                         |
#   |                        | |/ _` | '_ \| |/ _ \                        |
#   |                        | | (_| | |_) | |  __/                        |
#   |                        |_|\__,_|_.__/|_|\___|                        |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

def discover_vertiv_geist_pdu_phase(section) -> DiscoveryResult:
    for sensorlabel, sensordata in section['phase'].items():
        yield Service(item=sensorlabel)

def check_vertiv_geist_pdu_phase(item, params, section) -> CheckResult:
    if item in section['phase']:
        yield from check_elphase(item, params, section['phase'])

register.check_plugin(
    name="vertiv_geist_pdu_pdu_phase",
    sections=['vertiv_geist_pdu'],
    service_name="PDU Phase %s",
    discovery_function=discover_vertiv_geist_pdu_phase,
    check_function=check_vertiv_geist_pdu_phase,
    check_ruleset_name='ups_outphase',
    check_default_parameters={},
)
