#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2020 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de
#
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
    contains,
    register,
    render,
    Metric,
    OIDEnd,
    Result,
    Service,
    SNMPTree,
    State,
)

from .utils import temperature

def parse_wagner_racksens2(string_table):
    section = {
        'info': [
            ('Manufacturer', string_table[0][0][0]),
            ('Unit name', string_table[0][0][1]),
            ('Unit version', string_table[0][0][2]),
            ('Unit serial', string_table[1][0][0]),
        ],
        'airflow': (
            int(string_table[1][0][30]),
            float(string_table[1][0][9]),
            int(string_table[1][0][28]),
            int(string_table[1][0][29]),
        ),
        'temps': [
            ('Air', float(string_table[1][0][8]), None, None),
        ],
        'detectors': {},
        'alarms': {
            'Extinguishing': int(string_table[0][0][3]),
            'Cut Off': int(string_table[0][0][4]),
            'Manual': int(string_table[0][0][5]),
            'Failure': int(string_table[0][0][15]),
            'Service or Blocked': int(string_table[0][0][16]),
            'Door': int(string_table[0][0][17]),
            'Main': int(string_table[0][0][18]),
            },
        }
    for detector in [1, 2]:
        serial = int(string_table[1][0][detector])
        if serial > 0:
            section['detectors'][str(detector)] = {
                'serial': serial,
                'mainalarm': int(string_table[0][0][detector + 5]),
                'prealarm': int(string_table[0][0][detector + 7]),
                'smoke': float(string_table[1][0][detector + 9]),
                'chamber': int(string_table[1][0][detector + 20]),
            }
    for temp in [1, 2, 3, 4, 5]:
        if int(string_table[1][0][temp + 22]):
            section['temps'].append( (str(temp),
                                      float(string_table[1][0][temp + 2]),
                                      float(string_table[1][0][temp + 13]),
                                      int(string_table[0][0][temp + 9])) )
    return section

register.snmp_section(
    name="wagner_racksens2",
    detect=contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.34187.57949"),
    parse_function=parse_wagner_racksens2,
    fetch=[
        SNMPTree(
            base=".1.3.6.1.4.1.34187.57949.1.1",
            oids=[
                "1",      # RACKSENS2-MIB::rsManufacturer              0
                "2",      # RACKSENS2-MIB::rsUnitName                  1
                "3",      # RACKSENS2-MIB::rsUnitVersion               2
                "1000",   # RACKSENS2-MIB::pswExtinguishing            3
                "1001",   # RACKSENS2-MIB::pswCutOffActive             4
                "1002",   # RACKSENS2-MIB::pswManualActivation         5
                "1003",   # RACKSENS2-MIB::pswMainAlarmD1              6
                "1004",   # RACKSENS2-MIB::pswMainAlarmD2              7
                "1005",   # RACKSENS2-MIB::pswPreAlarmD1               8
                "1006",   # RACKSENS2-MIB::pswPreAlarmD2               9
                "1007",   # RACKSENS2-MIB::pswTemperatureAlarm1       10
                "1008",   # RACKSENS2-MIB::pswTemperatureAlarm2       11
                "1009",   # RACKSENS2-MIB::pswTemperatureAlarm3       12
                "1010",   # RACKSENS2-MIB::pswTemperatureAlarm4       13
                "1011",   # RACKSENS2-MIB::pswTemperatureAlarm5       14
                "1012",   # RACKSENS2-MIB::pswFailure                 15
                "1013",   # RACKSENS2-MIB::pswServiceOrBlocked        16
                "1014",   # RACKSENS2-MIB::pswDoorState               17
                "1015",   # RACKSENS2-MIB::pswUnitMainAlarm           18
            ]),
        SNMPTree(
            base=".1.3.6.1.4.1.34187.57949.2.1",
            oids=[
                "24577",  # RACKSENS2-MIB::rsUnitSerialNumber          0
                "24578",  # RACKSENS2-MIB::rsDetector1SerialNumber     1
                "24579",  # RACKSENS2-MIB::rsDetector2SerialNumber     2
                "245800000",  # RACKSENS2-MIB::rsTemperature1String    3
                "245810000",  # RACKSENS2-MIB::rsTemperature2String    4
                "245820000",  # RACKSENS2-MIB::rsTemperature3String    5
                "245830000",  # RACKSENS2-MIB::rsTemperature4String    6
                "245840000",  # RACKSENS2-MIB::rsTemperature5String    7
                "245850000",  # RACKSENS2-MIB::rsAirTemperatureString  8
                "245860000",  # RACKSENS2-MIB::rsAirFlowSpeedString    9
                "245940000",  # RACKSENS2-MIB::rsSmokeLevel1String    10
                "245990000",  # RACKSENS2-MIB::rsSmokeLevel2String    11
                "246050000",  # RACKSENS2-MIB::rsSensibility1String   12
                "246060000",  # RACKSENS2-MIB::rsSensibility2String   13
                "246070000",  # RACKSENS2-MIB::rsAlarmTemp1String     14
                "246080000",  # RACKSENS2-MIB::rsAlarmTemp2String     15
                "246090000",  # RACKSENS2-MIB::rsAlarmTemp3String     16
                "246100000",  # RACKSENS2-MIB::rsAlarmTemp4String     17
                "246110000",  # RACKSENS2-MIB::rsAlarmTemp5String     18
                "246120000",  # RACKSENS2-MIB::rsFanVoltageString     19
                "246260000",  # RACKSENS2-MIB::rsFlowReferenceString  20
                "24595",  # RACKSENS2-MIB::rsChamberState1            21
                "24600",  # RACKSENS2-MIB::rsChamberState2            22
                "24590037", # RACKSENS2-MIB::rsTempSensor1Registrated 23
                "24590038", # RACKSENS2-MIB::rsTempSensor2Registrated 24
                "24590039", # RACKSENS2-MIB::rsTempSensor3Registrated 25
                "24590040", # RACKSENS2-MIB::rsTempSensor4Registrated 26
                "24590041", # RACKSENS2-MIB::rsTempSensor5Registrated 27
                "24587",  # RACKSENS2-MIB::rsAirFlowdeviation         28
                "24602",  # RACKSENS2-MIB::rsAirFlowFailureThreshold  29
                "24590042", # RACKSENS2-MIB::rsAirFlowControlAvailable 30
            ]),
    ],
)

#.
#   .--info----------------------------------------------------------------.
#   |                          _        __                                 |
#   |                         (_)_ __  / _| ___                            |
#   |                         | | '_ \| |_ / _ \                           |
#   |                         | | | | |  _| (_) |                          |
#   |                         |_|_| |_|_|  \___/                           |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'

def discover_wagner_racksens2_info(section):
    if 'info' in section:
        yield Service()

def check_wagner_racksens2_info(section):
    for key, value in section.get('info', []):
        yield Result(state=State.OK,
                     summary="%s: %s" % (key, value))

register.check_plugin(
    name="wagner_racksens2_info",
    sections=['wagner_racksens2'],
    service_name="Racksens2 Info",
    discovery_function=discover_wagner_racksens2_info,
    check_function=check_wagner_racksens2_info,
)

#.
#   .--detector------------------------------------------------------------.
#   |                    _      _            _                             |
#   |                 __| | ___| |_ ___  ___| |_ ___  _ __                 |
#   |                / _` |/ _ \ __/ _ \/ __| __/ _ \| '__|                |
#   |               | (_| |  __/ ||  __/ (__| || (_) | |                   |
#   |                \__,_|\___|\__\___|\___|\__\___/|_|                   |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'

def discover_wagner_racksens2_detector(section):
    for d in section.get('detectors', {}).keys():
        yield Service(item=d)

def check_wagner_racksens2_detector(item, params, section):
    for d, vals in section.get('detectors', {}).items():
        if item == d:
            yield Result(state=State.OK,
                         summary="Serial: %d" % vals['serial'])
            if vals['prealarm']:
                yield Result(state=State.WARN, summary="Action Alarm")
            if vals['mainalarm']:
                yield Result(state=State.CRIT, summary="Fire Alarm")
            yield from check_levels(
                vals['smoke'],
                levels_upper=params.get('smoke_levels'),
                metric_name="smoke_perc",
                label="Smoke detected",
                render_func=render.percent,
            )
            levels_lower = params.get('chamber_levels')
            if isinstance(levels_lower, tuple):
                warn, crit = levels_lower
                levels_lower = (-warn, -crit)
            yield from check_levels(
                vals['chamber'],
                levels_upper=params.get('chamber_levels'),
                levels_lower=levels_lower,
                metric_name="chamber_perc",
                label="Chamber Deviation",
                render_func=render.percent,
            )

register.check_plugin(
    name="wagner_racksens2_detector",
    sections=['wagner_racksens2'],
    service_name="Racksens2 Detector %s",
    discovery_function=discover_wagner_racksens2_detector,
    check_function=check_wagner_racksens2_detector,
    check_default_parameters={
        "smoke_levels": (3, 5),
        "chamber_levels": (10, 20),
    }
)

#.
#   .--temperature---------------------------------------------------------.
#   |      _                                      _                        |
#   |     | |_ ___ _ __ ___  _ __   ___ _ __ __ _| |_ _   _ _ __ ___       |
#   |     | __/ _ \ '_ ` _ \| '_ \ / _ \ '__/ _` | __| | | | '__/ _ \      |
#   |     | ||  __/ | | | | | |_) |  __/ | | (_| | |_| |_| | | |  __/      |
#   |      \__\___|_| |_| |_| .__/ \___|_|  \__,_|\__|\__,_|_|  \___|      |
#   |                       |_|                                            |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'

def discover_wagner_racksens2_temp(section):
    for temp in section.get('temps', []):
        yield Service(item=temp[0])

def check_wagner_racksens2_temp(item, params, section):
    for temp in section.get('temps', []):
        if temp[0] == item:
            if temp[2] is None or temp[3] is None:
                yield from temperature.check_temperature(
                    temp[1],
                    params,
                )
            else:
                yield from temperature.check_temperature(
                    temp[1],
                    params,
                    dev_levels = (temp[2], temp[2]),
                    dev_status = temp[3] * 2,
                    dev_status_name = 'Alarm',
                )

register.check_plugin(
    name="wagner_racksens2_temp",
    sections=['wagner_racksens2'],
    service_name="Racksens2 Temp %s",
    discovery_function=discover_wagner_racksens2_temp,
    check_function=check_wagner_racksens2_temp,
    check_default_parameters={},
    check_ruleset_name="temperature",
)

#.
#   .--alarms--------------------------------------------------------------.
#   |                        _                                             |
#   |                   __ _| | __ _ _ __ _ __ ___  ___                    |
#   |                  / _` | |/ _` | '__| '_ ` _ \/ __|                   |
#   |                 | (_| | | (_| | |  | | | | | \__ \                   |
#   |                  \__,_|_|\__,_|_|  |_| |_| |_|___/                   |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'

def discover_wagner_racksens2_alarm(section):
    for alarm in section.get('alarms', {}).keys():
        yield Service(item=alarm)

def check_wagner_racksens2_alarm(item, section):
    map_status = {
        0: State.OK,
        1: State.CRIT,
    }
    if item in section.get('alarms', {}):
        status = map_status.get(section['alarms'][item], State.UNKNOWN)
        yield Result(state=status, summary="Status: %d" % section['alarms'][item])

register.check_plugin(
    name="wagner_racksens2_alarm",
    sections=['wagner_racksens2'],
    service_name="Racksens2 Alarm %s",
    discovery_function=discover_wagner_racksens2_alarm,
    check_function=check_wagner_racksens2_alarm,
)

#.
#   .--air flow deviation--------------------------------------------------.
#   |              _         __ _                     _                    |
#   |         __ _(_)_ __   / _| | _____      __   __| | _____   __        |
#   |        / _` | | '__| | |_| |/ _ \ \ /\ / /  / _` |/ _ \ \ / /        |
#   |       | (_| | | |    |  _| | (_) \ V  V /  | (_| |  __/\ V /         |
#   |        \__,_|_|_|    |_| |_|\___/ \_/\_/    \__,_|\___| \_/          |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'

def discover_wagner_racksens2_airflow(section):
    if section['airflow'][0]:
        yield Service()

def check_wagner_racksens2_airflow(section):
    airflow = section['airflow']
    if airflow[0]:
        yield Result(state=State.OK,
                     summary="%0.4f m/s" % airflow[1])
        yield Metric('airflow_meter', airflow[1])
        yield from check_levels(
            airflow[2],
            levels_upper=(None, airflow[3]),
            levels_lower=(None, -airflow[3]),
            metric_name='deviation_airflow',
            label='Deviation',
            render_func=render.percent,
        )

register.check_plugin(
    name="wagner_racksens2_airflow",
    sections=['wagner_racksens2'],
    service_name="Racksens2 Airflow",
    discovery_function=discover_wagner_racksens2_airflow,
    check_function=check_wagner_racksens2_airflow,
)
