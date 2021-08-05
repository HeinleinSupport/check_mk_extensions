#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Description of OIDs used from RFC 1628
#   upsAlarm              OBJECT IDENTIFIER ::= { upsObjects 6 }
#
#   upsAlarmsPresent OBJECT-TYPE
#       SYNTAX     Gauge32
#       MAX-ACCESS read-only
#       STATUS     current
#       DESCRIPTION
#               "The present number of active alarm conditions."
#       ::= { upsAlarm 1 }
#
#   upsAlarmTable OBJECT-TYPE
#       SYNTAX     SEQUENCE OF UpsAlarmEntry
#       MAX-ACCESS not-accessible
#       STATUS     current
#       DESCRIPTION
#               "A list of alarm table entries.  The table contains
#               zero, one, or many rows at any moment, depending upon
#               the number of alarm conditions in effect.  The table
#               is initially empty at agent startup.  The agent
#               creates a row in the table each time a condition is
#               detected and deletes that row when that condition no
#               longer pertains.  The agent creates the first row with
#               upsAlarmId equal to 1, and increments the value of
#               upsAlarmId each time a new row is created, wrapping to
#               the first free value greater than or equal to 1 when
#               the maximum value of upsAlarmId would otherwise be
#               exceeded.  Consequently, after multiple operations,
#               the table may become sparse, e.g., containing entries
#               for rows 95, 100, 101, and 203 and the entries should
#               not be assumed to be in chronological order because
#               upsAlarmId might have wrapped.
#
#               Alarms are named by an AutonomousType (OBJECT
#               IDENTIFIER), upsAlarmDescr, to allow a single table to
#               reflect well known alarms plus alarms defined by a
#               particular implementation, i.e., as documented in the
#               private enterprise MIB definition for the device.  No
#               two rows will have the same value of upsAlarmDescr,
#               since alarms define conditions.  In order to meet this
#               requirement, care should be taken in the definition of
#               alarm conditions to insure that a system cannot enter
#               the same condition multiple times simultaneously.
#
#               The number of rows in the table at any given time is
#               reflected by the value of upsAlarmsPresent."
#       ::= { upsAlarm 2 }

from .agent_based_api.v1 import (
    any_of,
    contains,
    register,
    render,
    Result,
    Service,
    SNMPTree,
    State,
)
from .utils.ups import DETECT_UPS_GENERIC

def parse_snmp_uptime(ticks):
    if len(ticks) < 3:
        return 0

    try:
        return int(ticks[:-2])
    except Exception:
        pass

    try:
        days, h, m, s = ticks.split(":")
        return (int(days) * 86400) + (int(h) * 3600) + (int(m) * 60) + int(float(s))
    except Exception:
        pass

    return 0

def parse_ups_alarms(string_table):
    transUpsAlarm = { '.1.3.6.1.2.1.33.1.6.3.1': 'Battery Bad',
                      '.1.3.6.1.2.1.33.1.6.3.2': 'On Battery',
                      '.1.3.6.1.2.1.33.1.6.3.3': 'Low Battery',
                      '.1.3.6.1.2.1.33.1.6.3.4': 'Depleted Battery',
                      '.1.3.6.1.2.1.33.1.6.3.5': 'Temperature Bad',
                      '.1.3.6.1.2.1.33.1.6.3.6': 'Input Bad',
                      '.1.3.6.1.2.1.33.1.6.3.7': 'Output Bad',
                      '.1.3.6.1.2.1.33.1.6.3.8': 'Output Overload',
                      '.1.3.6.1.2.1.33.1.6.3.9': 'On Bypass',
                      '.1.3.6.1.2.1.33.1.6.3.10': 'Bypass Bad',
                      '.1.3.6.1.2.1.33.1.6.3.11': 'Output Off As Requested',
                      '.1.3.6.1.2.1.33.1.6.3.12': 'Ups Off As Requested',
                      '.1.3.6.1.2.1.33.1.6.3.13': 'Charger Failed',
                      '.1.3.6.1.2.1.33.1.6.3.14': 'Ups Output Off',
                      '.1.3.6.1.2.1.33.1.6.3.15': 'Ups System Off',
                      '.1.3.6.1.2.1.33.1.6.3.16': 'Fan Failure',
                      '.1.3.6.1.2.1.33.1.6.3.17': 'Fuse Failure',
                      '.1.3.6.1.2.1.33.1.6.3.18': 'General Fault',
                      '.1.3.6.1.2.1.33.1.6.3.19': 'Diagnostic Test Failed',
                      '.1.3.6.1.2.1.33.1.6.3.20': 'Communications Lost',
                      '.1.3.6.1.2.1.33.1.6.3.21': 'Awaiting Power',
                      '.1.3.6.1.2.1.33.1.6.3.22': 'Shutdown Pending',
                      '.1.3.6.1.2.1.33.1.6.3.23': 'Shutdown Imminent',
                      '.1.3.6.1.2.1.33.1.6.3.24': 'Test In Progress',
    }
    section = {'count': 0}

    if len(string_table) == 2:
        if len(string_table[0]) == 1:
            section['count'] = int(string_table[0][0][0])
        if len(string_table[1]) > 0 and section['count'] > 0:
            section['alarms'] = []
            for line in string_table[1]:
                section['alarms'].append((parse_snmp_uptime(line[1]), transUpsAlarm.get(line[0], 'Unknown')))
    return section

register.snmp_section(
    name="ups_alarms",
    detect=any_of(
        DETECT_UPS_GENERIC,
        contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.318.1.3.27"),
    ),
    parse_function=parse_ups_alarms,
    fetch=[
        SNMPTree(
            base=".1.3.6.1.2.1.33.1.6",
            oids=["1.0"]
        ),
        SNMPTree(
            base=".1.3.6.1.2.1.33.1.6.2.1",
            oids=["2", "3"]
        ),
    ],
)

def discover_ups_alarms(section_ups_alarms, section_uptime):
    if section_ups_alarms:
        yield Service()

def check_ups_alarms(section_ups_alarms, section_uptime):
    if section_ups_alarms['count'] > 0:
        alarms = []
        for alarm in section_ups_alarms['alarms']:
            alarms.append("%s (was %s ago)" % (alarm[1],
                                               render.timespan(section_uptime.uptime_sec - alarm[0])))
        yield Result(state=State.CRIT,
                     summary='%d Alarms found (see long output)' % section_ups_alarms['count'],
                     details="\n".join(alarms))
    else:
        yield Result(state=State.OK,
                     summary="No Alarms present")

register.check_plugin(
    name='ups_alarms',
    sections=['ups_alarms', 'uptime'],
    service_name="UPS Alarms",
    discovery_function=discover_ups_alarms,
    check_function=check_ups_alarms,
)
