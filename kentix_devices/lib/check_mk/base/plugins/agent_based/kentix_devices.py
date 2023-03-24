#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2018 Heinlein Support GmbH
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

from typing import NamedTuple

from .agent_based_api.v1 import (
    any_of,
    contains,
    check_levels,
    register,
    render,
    Metric,
    OIDEnd,
    Result,
    Service,
    ServiceLabel,
    SNMPTree,
    State,
)

from .agent_based_api.v1.type_defs import (
    CheckResult,
    DiscoveryResult,
)

from .utils.temperature import (
    check_temperature,
)

from .utils.humidity import (
    check_humidity,
)

import time

def _get_dev_status_kentix_devices(alarm):
    alarm_state_map = { "1": State.CRIT,
                        "2": State.WARN,
    }
    return alarm_state_map.get(alarm, State.OK)

def parse_kentix_devices(string_table):
    section = {'multiplier': list(map(float, string_table[0][0])),
              'sensors': {},
              'zones': {} }
    meta = { 3: 'temp',
             4: 'humidity',
             5: 'dewpoint',
             6: 'co',
             7: 'motion',
             8: 'vibration',
             # 9: 'latency'
           }
    armed = { '0': False,
              '1': True,
            }
    for line in string_table[1]:
        section['zones'][line[0]] = {'name': line[1], 'armed': armed.get(line[2], False)}
    for line in string_table[2]:
        sid = line[0]
        sensor = { 'info': line }
        sensor['type'] = line[2]
        sensor['zone'] = line[6]
        for key, val in meta.items():
            for subline in string_table[key]:
                if subline[0] == sid:
                    sensor[val] = subline
        section['sensors']["%s %s" % (line[1], sid)] = sensor
    return section

register.snmp_section(
    name="kentix_devices",
    parse_function=parse_kentix_devices,
    fetch=[
        SNMPTree(
            base=".1.3.6.1.4.1.37954.5.1.1",
            oids=[
                "1.0", # 0 multiplierTemperature
                "2.0", # 1 multiplierHumidity
                "3.0", # 2 multiplierDewpoint
                # "5.0", # 3 multiplierVoltage
                # "6.0", # 4 multiplierCurrent
                # "7.0", # 5 multiplierActivepower
                # "8.0", # 6 multiplierReactivepower
                # "9.0", # 7 multiplierApparent
                # "10.0", # 8 multiplierFrequency
                # "11.0", # 9 multiplierConsumption
                # "12.0", # 10 multiplierPue
                # "13.0", # 11 valuemultiplier.13
            ]),
        SNMPTree(
            base=".1.3.6.1.4.1.37954.5.3.1.1",
            oids=[
                "1",      # zoneIndex
                "2",      # zoneName
                "3",      # zoneArmedState
            ]),
        SNMPTree(
            base=".1.3.6.1.4.1.37954.5.2.1.1",
            oids=[
                "1",      # generalIndex
                "2",      # sensorName
                "3",      # sensorType
                "4",      # sensorVersion
                "5",      # sensorAddress
                "6",      # sensorPort
                "7",      # sensorZone
                "8",      # sensorCommunication
                "9",      # sensorBatteryLevel (only used for battery sensors)
            ] ),
        SNMPTree(
            base=".1.3.6.1.4.1.37954.5.2.2.1",
            oids=[
                "1",      # temperatureIndex
                "2",      # tempValue
                "4",      # tempMin
                "5",      # tempMax
                "3",      # tempAlarm
            ] ),
        SNMPTree(
            base=".1.3.6.1.4.1.37954.5.2.3.1",
            oids=[
                "1",      # humidityIndex
                "2",      # humValue
                "5",      # humMax
                "3",      # humAlarm
            ] ),
        SNMPTree(
            base=".1.3.6.1.4.1.37954.5.2.4.1",
            oids=[
                "1",      # dewpointIndex
                "2",      # dewValue
                "5",      # dewMax
                "3",      # dewAlarm
            ] ),
        SNMPTree(
            base=".1.3.6.1.4.1.37954.5.2.5.1",
            oids=[
                "1",      # coIndex
                "2",      # coValue
                "5",      # coMax
                "3",      # coAlarm
            ] ),
        SNMPTree(
            base=".1.3.6.1.4.1.37954.5.2.6.1",
            oids=[
                "1",      # motionIndex
                "2",      # motValue
                "5",      # motMax
                "3",      # motAlarm
            ] ),
        SNMPTree(
            base=".1.3.6.1.4.1.37954.5.2.7.1",
            oids=[
                "1",      # vibrationIndex
                "2",      # vibValue
                "5",      # vibMax
                "3",      # vibAlarm
            ] ),
#        SNMPTree( ".1.3.6.1.4.1.37954.5.2.8.1", [ "1",      # latencyIndex
#                                      "2",      # latValue
#                                      # "3",      # latAlarm
#                                      "5",      # latMax
#                                    ] ),
        ],
    detect=any_of(
        contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.37954.5"),
        contains(".1.3.6.1.2.1.1.1.0", "kentix"),
    ),
)

def discover_kentix_devices(section, params, sfunc) -> DiscoveryResult:
    for sensoritem, sensordata in section['sensors'].items():
        if sfunc in sensordata:
            sl = []
            if sensordata['zone'] in section['zones']:
                sl.append( ServiceLabel('kentix/zoneid', sensordata['zone']) )
            yield Service(
                item=sensoritem,
                parameters=params,
                labels=sl,
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

def check_kentix_devices_temperature(item, params, section):
    if item in section['sensors']:
        sensordata = section['sensors'][item]
        tempMin = float(sensordata['temp'][2])
        tempMax = float(sensordata['temp'][3])
        dev_status = _get_dev_status_kentix_devices(sensordata['temp'][4])
        yield from check_temperature(float(sensordata['temp'][1]) / section['multiplier'][0],
                                     params,
                                     dev_levels=(tempMax, tempMax),
                                     dev_levels_lower=(tempMin, tempMin),
                                     dev_status=dev_status,
        )
        zone = ""
        if sensordata['zone'] in section['zones']:
            yield Result(state=State.OK,
                         summary="Zone: %s" % section['zones'][sensordata['zone']]['name'])

register.check_plugin(
    name="kentix_devices",
    sections=['kentix_devices'],
    service_name="Temperature %s",
    discovery_function=lambda section: (yield from discover_kentix_devices(
        section,
        {},
        'temp'
    )),
    check_function=check_kentix_devices_temperature,
    check_ruleset_name='temperature',
    check_default_parameters={}, #  "levels": (40, 50) },
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


def check_kentix_devices_humidity(item, params, section):
    if item in section['sensors']:
        sensordata = section['sensors'][item]
        dev_status = _get_dev_status_kentix_devices(sensordata['humidity'][3])
        yield Result(state=dev_status,
                     notice="Device Status: %s" % sensordata['humidity'][3])
        if not params:
            params = { 'levels': ( float(sensordata['humidity'][2]), 101 ) }
        yield from check_humidity(
            float(sensordata['humidity'][1]) / section['multiplier'][1],
            params
        )
        zone = ""
        if sensordata['zone'] in section['zones']:
            yield Result(state=State.OK,
                         summary="Zone: %s" % section['zones'][sensordata['zone']]['name'])

register.check_plugin(
    name="kentix_devices_humidity",
    sections=['kentix_devices'],
    service_name="Humidity %s",
    discovery_function=lambda section: (yield from discover_kentix_devices(
        section,
        {},
        'humidity'
    )),
    check_function=check_kentix_devices_humidity,
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

def check_kentix_devices_dewpoint(item, params, section):
    if item in section['sensors']:
        sensordata = section['sensors'][item]
        dewValue = float(sensordata['dewpoint'][1]) / section['multiplier'][2]
        dewMax = float(sensordata['dewpoint'][2])
        dev_status = _get_dev_status_kentix_devices(sensordata['dewpoint'][3])
        if 'temp' in sensordata:
            tempValue = float(sensordata['temp'][1]) / section['multiplier'][0]
            yield from check_temperature(dewValue,
                                         params,
                                         dev_levels=(tempValue - dewMax, tempValue - dewMax),
                                         dev_status=dev_status,
            )
        else:
            yield from check_temperature(dewValue,
                                         params,
                                         dev_status=dev_status,
            )
        zone = ""
        if sensordata['zone'] in section['zones']:
            yield Result(state=State.OK,
                         summary="Zone: %s" % section['zones'][sensordata['zone']]['name'])

register.check_plugin(
    name="kentix_devices_dewpoint",
    sections=['kentix_devices'],
    service_name="Dewpoint %s",
    discovery_function=lambda section: (yield from discover_kentix_devices(
        section,
        {},
        'dewpoint'
    )),
    check_function=check_kentix_devices_dewpoint,
    check_ruleset_name='temperature',
    check_default_parameters={},
)

#.
#   .--CO - carbon monoxide------------------------------------------------.
#   |         ____ ___                           _                         |
#   |        / ___/ _ \            ___ __ _ _ __| |__   ___  _ __          |
#   |       | |  | | | |  _____   / __/ _` | '__| '_ \ / _ \| '_ \         |
#   |       | |__| |_| | |_____| | (_| (_| | |  | |_) | (_) | | | |        |
#   |        \____\___/           \___\__,_|_|  |_.__/ \___/|_| |_|        |
#   |                                                                      |
#   |                                            _     _                   |
#   |            _ __ ___   ___  _ __   _____  _(_) __| | ___              |
#   |           | '_ ` _ \ / _ \| '_ \ / _ \ \/ / |/ _` |/ _ \             |
#   |           | | | | | | (_) | | | | (_) >  <| | (_| |  __/             |
#   |           |_| |_| |_|\___/|_| |_|\___/_/\_\_|\__,_|\___|             |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'


def check_kentix_devices_co(item, section):
    if item in section['sensors']:
        sensordata = section['sensors'][item]
        coValue = int(sensordata['co'][1])
        coMax = int(sensordata['co'][2])
        dev_status = _get_dev_status_kentix_devices(sensordata['co'][3])
        state = State.OK
        if coValue > coMax:
            state = State.CRIT
        yield Result(state=State.worst(state, dev_status),
                     summary="%d ppm" % coValue)
        yield Metric('parts_per_million', coValue, levels=(None, coMax))
        if sensordata['zone'] in section['zones']:
            yield Result(state=State.OK,
                         summary="Zone: %s" % section['zones'][sensordata['zone']]['name'])

register.check_plugin(
    name="kentix_devices_co",
    sections=['kentix_devices'],
    service_name="CO %s",
    discovery_function=lambda section: (yield from discover_kentix_devices(
        section,
        {},
        'co'
    )),
    check_function=check_kentix_devices_co,
)

#.
#   .--motion--------------------------------------------------------------.
#   |                                  _   _                               |
#   |                  _ __ ___   ___ | |_(_) ___  _ __                    |
#   |                 | '_ ` _ \ / _ \| __| |/ _ \| '_ \                   |
#   |                 | | | | | | (_) | |_| | (_) | | | |                  |
#   |                 |_| |_| |_|\___/ \__|_|\___/|_| |_|                  |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'


def check_kentix_devices_motion(item, params, section):
    def test_in_period(hour, minute, periods):
        time_mins = hour * 60 + minute
        for per in periods:
            per_mins_low  = per[0][0] * 60 + per[0][1]
            per_mins_high = per[1][0] * 60 + per[1][1]
            if time_mins >= per_mins_low and time_mins < per_mins_high:
                return True
        return False

    if item in section['sensors']:
        sensordata = section['sensors'][item]
        motionValue = int(sensordata['motion'][1])
        motionMax = int(sensordata['motion'][2])
        dev_status = _get_dev_status_kentix_devices(sensordata['motion'][3])

        weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        today = time.localtime()
        if params != None and 'time_periods' in params:
            periods = params['time_periods'][weekdays[today.tm_wday]]
        else:
            periods = [((0, 0), (24, 0))]

        zone = ''
        zoneArmed = True
        if sensordata['zone'] in section['zones']:
            zone = " in zone %s" % section['zones'][sensordata['zone']]['name']
            zoneArmed = section['zones'][sensordata['zone']]['armed']
        if motionValue >= motionMax:
            state = State.OK
            if zoneArmed:
                state = test_in_period(today.tm_hour, today.tm_min, periods) and State.WARN or State.OK
            yield Result(state=State.worst(state, dev_status),
                         summary='Motion detected%s' % zone)
            
        else:
            yield Result(state=dev_status,
                         summary="No motion%s detected" %zone)
        yield Metric('motion', motionValue, levels=(motionMax, None), boundaries=(0, 100))

register.check_plugin(
    name="kentix_devices_motion",
    sections=['kentix_devices'],
    service_name="Motion %s",
    discovery_function=lambda section: (yield from discover_kentix_devices(
        section,
        {},
        'motion'
    )),
    check_function=check_kentix_devices_motion,
    check_ruleset_name="motion",
    check_default_parameters={},
)

#.
#   .--vibration-----------------------------------------------------------.
#   |                    _ _               _   _                           |
#   |             __   _(_) |__  _ __ __ _| |_(_) ___  _ __                |
#   |             \ \ / / | '_ \| '__/ _` | __| |/ _ \| '_ \               |
#   |              \ V /| | |_) | | | (_| | |_| | (_) | | | |              |
#   |               \_/ |_|_.__/|_|  \__,_|\__|_|\___/|_| |_|              |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'


def check_kentix_devices_vibration(item, section):
    if item in section['sensors']:
        sensordata = section['sensors'][item]
        vibrationValue = int(sensordata['vibration'][1])
        vibrationMax = int(sensordata['vibration'][2])
        dev_status = _get_dev_status_kentix_devices(sensordata['vibration'][3])
        state = State.OK
        if vibrationValue >= vibrationMax:
            state = State.CRIT
        zone = ""
        if sensordata['zone'] in section['zones']:
            zone = " in zone %s" % section['zones'][sensordata['zone']]['name']
        yield Result(state=State.worst(state, dev_status),
                     summary="%d%s" % (vibrationValue, zone))
        yield Metric('vibration', vibrationValue, levels=(None, vibrationMax))

register.check_plugin(
    name="kentix_devices_vibration",
    sections=['kentix_devices'],
    service_name="Vibration %s",
    discovery_function=lambda section: (yield from discover_kentix_devices(
        section,
        {},
        'vibration'
    )),
    check_function=check_kentix_devices_vibration,
)

#.
#   .--zones---------------------------------------------------------------.
#   |                                                                      |
#   |                      _______  _ __   ___  ___                        |
#   |                     |_  / _ \| '_ \ / _ \/ __|                       |
#   |                      / / (_) | | | |  __/\__ \                       |
#   |                     /___\___/|_| |_|\___||___/                       |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'

def discover_kentix_devices_zone(section):
    for zoneid, zoneinfo in section['zones'].items():
        sl = [ ServiceLabel('kentix/zoneid', zoneid) ]
        yield Service(item=zoneid + " " + zoneinfo['name'],
                      parameters={'armed': zoneinfo['armed']},
                      labels=sl
        )

def check_kentix_devices_zone(item, params, section):
    zoneid = item.split()[0]
    if zoneid in section['zones']:
        zoneinfo = section['zones'][zoneid]
        state = State.OK
        text = "armed = %s" % zoneinfo['armed']
        if params.get('armed') != zoneinfo['armed']:
            state = State.WARN
            text += ', was %s at discovery' % params.get('armed')
        yield Result(state=state,
                     summary=text)

register.check_plugin(
    name="kentix_devices_zone",
    sections=['kentix_devices'],
    service_name="Zone %s",
    discovery_function=discover_kentix_devices_zone,
    check_function=check_kentix_devices_zone,
    check_default_parameters={},
)

#   .--battery-------------------------------------------------------------.
#   |                                                                      |
#   |                  _           _   _                                   |
#   |                 | |__   __ _| |_| |_ ___ _ __ _   _                  |
#   |                 | '_ \ / _` | __| __/ _ \ '__| | | |                 |
#   |                 | |_) | (_| | |_| ||  __/ |  | |_| |                 |
#   |                 |_.__/ \__,_|\__|\__\___|_|   \__, |                 |
#   |                                               |___/                  |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'

def battery_supported(devicetype):
    battery_devicetypes = [28, 26]
    return devicetype in battery_devicetypes

def discover_kentix_devices_battery(section):
    for sensoritem, sensordata in section['sensors'].items():
        if battery_supported(int(sensordata['type'])):
            yield Service(
                item=sensoritem
            )

def check_kentix_devices_battery(item, section):
    if item in section['sensors']:
        sensordata = section['sensors'][item]
        batterystatus = int(sensordata['info'][8])
        summary = "Battery OK."
        state = State.OK
        if batterystatus != 0:
            summary = "Battery not ok."
            state = State.CRIT
        yield Result(state=state, summary=summary)

register.check_plugin(
    name="kentix_devices_battery",
    sections=['kentix_devices'],
    service_name="Battery %s",
    discovery_function=discover_kentix_devices_battery,
    check_function=check_kentix_devices_battery,
)

#   .--inputs--------------------------------------------------------------.
#   |                     _                   _                            |
#   |                    (_)_ __  _ __  _   _| |_ ___                      |
#   |                    | | '_ \| '_ \| | | | __/ __|                     |
#   |                    | | | | | |_) | |_| | |_\__ \                     |
#   |                    |_|_| |_| .__/ \__,_|\__|___/                     |
#   |                            |_|                                       |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

_MAX_INPUT_SENSORS = 16

def parse_kentix_devices_inputs(string_table):
    section = {}
    for inputline in range(_MAX_INPUT_SENSORS):
        if string_table[inputline]:
            section[inputline + 1] = string_table[inputline]
        else:
            section[inputline + 1] = None
    return section

register.snmp_section(
    name="kentix_devices_inputs",
    parse_function=parse_kentix_devices_inputs,
    fetch=[
        SNMPTree(
            base=".1.3.6.1.4.1.37954.5.2.100.%d.1" % i,
            oids=[
                # "1", # KENTIXDEVICES::input1Index
                "2", # KENTIXDEVICES::input1Name
                "3", # KENTIXDEVICES::input1Zone
                # "4", # KENTIXDEVICES::input1Value
                "5", # KENTIXDEVICES::input1Alarm
            ] )
        for i in range(1, _MAX_INPUT_SENSORS + 1)
        ],
    detect=any_of(
        contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.37954.5"),
        contains(".1.3.6.1.2.1.1.1.0", "kentix"),
    ),
)

def discover_kentix_devices_inputs(section):
    for inputline in section:
        if section[inputline]:
            yield Service(item="%d" % inputline)

def check_kentix_devices_inputs(item, section):
    item = int(item)
    if section.get(item):
        for data in section[item]:
            yield Result(state=_get_dev_status_kentix_devices(data[2]),
                         summary="%s in Zone %s" % (data[0], data[1]))

register.check_plugin(
    name="kentix_devices_inputs",
    sections=['kentix_devices_inputs'],
    service_name="Input %s",
    discovery_function=discover_kentix_devices_inputs,
    check_function=check_kentix_devices_inputs,
)
