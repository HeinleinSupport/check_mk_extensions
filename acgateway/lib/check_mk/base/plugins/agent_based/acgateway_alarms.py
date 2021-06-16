#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2019 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>

#
# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

def inventory_acgateway_alarms(info):
    if len(info) == 2:
        yield None, {}

def check_acgateway_alarms(_no_item, params, info):
    for line in info[0]:
        yield 2, "ALARM#%s: %s, source: %s, uptime: %s" % (line[0], line[4], line[5], get_age_human_readable(saveint(line[1])))
    if len(info[0]) == 0:
        yield 0, "No active alarms present"
    yield 0, "%d alarms archived" % len(info[1])

# check_info['acgateway_alarms'] = {
#     'inventory_function'    : inventory_acgateway_alarms,
#     'check_function'        : check_acgateway_alarms,
#     'service_description'   : 'SIP Alarms',
#     'has_perfdata'          : False,
#     'snmp_info'             : [ ( '.1.3.6.1.4.1.5003.11.1.1.1.1',
#                                 [ '1', # AcAlarm::acActiveAlarmSequenceNumber
#                                   '2', # AcAlarm::acActiveAlarmSysuptime
#                                   '4', # AcAlarm::acActiveAlarmDateAndTime
#                                   '5', # AcAlarm::acActiveAlarmName
#                                   '6', # AcAlarm::acActiveAlarmTextualDescription
#                                   '7', # AcAlarm::acActiveAlarmSource
#                                   '8', # AcAlarm::acActiveAlarmSeverity
#                                 ]
#                               ),
#                                 ( '.1.3.6.1.4.1.5003.11.1.2.1.1',
#                                 [ '1', # AcAlarm::acAlarmHistorySequenceNumber
#                                 ] ) ],
#     'snmp_scan_function'    : lambda oid: oid('.1.3.6.1.2.1.1.2.0').startswith('.1.3.6.1.4.1.5003.8.1.1'),
# }
