#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2021 Heinlein Support GmbH
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

from .agent_based_api.v1 import (
    all_of,
    contains,
    get_rate,
    get_value_store,
    register,
    render,
    Metric,
    OIDEnd,
    Result,
    Service,
    SNMPTree,
    State,
)

import time

def parse_acgateway_calls(string_table):
    section = None
    if len(string_table) == 1:
        for active_calls, total_calls, asr, acd in string_table:
            section = {
                'active_calls': int(active_calls),
                'total_calls': int(total_calls),
                'asr': int(asr),
                'acd': int(acd),
            }
    return section

register.snmp_section(
    name="acgateway_calls",
    detect=all_of(
        contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.5003.8.1.1"),
        contains(".1.3.6.1.2.1.1.1.0", "SW Version: 7.20A"),
    ),
    parse_function=parse_acgateway_calls,
    fetch=SNMPTree(
        base='.1.3.6.1.4.1.5003.10.8.2',
        oids=[
            "52.43.1.2.0",   # AC-PM-Control-MIB::acPMSIPSBCEstablishedCallsVal.0
            "52.43.1.9.0",   # AC-PM-Control-MIB::acPMSIPSBCEstablishedCallsTotal.0
            "54.49.1.2.0",   # AC-PM-Control-MIB::acPMSBCAsrVal.0
            "54.52.1.2.0",   # AC-PM-Control-MIB::acPMSBCAcdVal.0
        ]),
)

def discover_acgateway_calls(section):
    yield Service()

def check_acgateway_calls(section):
    vs = get_value_store()
    now = time.time()
    yield Result(state=State.OK,
                 summary="Active Calls: %d" % section['active_calls'])
    yield Metric('active_calls', section['active_calls'])
    call_rate = get_rate(vs, 'acgateway_calls.total_calls', now, section['total_calls'])
    yield Result(state=State.OK,
                 summary="Calls per Second: %d/s" % call_rate)
    yield Metric('calls_per_sec', call_rate)
    yield Result(state=State.OK,
                 summary="Average Succes Ratio: %s" % render.percent(section['asr']))
    yield Metric('average_success_ratio', section['asr'])
    yield Result(state=State.OK,
                 summary="Average Call Duration: %s" % render.timespan(section['acd']))
    yield Metric('average_call_duration', section['acd'])

register.check_plugin(
    name="acgateway_calls",
    service_name="SBC Calls",
    discovery_function=discover_acgateway_calls,
    check_function=check_acgateway_calls,
)
