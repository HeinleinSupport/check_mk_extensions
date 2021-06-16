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

def inventory_acgateway_sipperf(info):
    if len(info) == 2:
        yield None, {}

def check_acgateway_sipperf(_no_item, params, info):
    sipperf_info = {
        0:  ("sip_calls_attempted", "Number of Attempted SIP/H323 calls"),
        1:  ("sip_calls_established", "Number of established (connected and voice activated) SIP/H323 calls"),
        2:  ("sip_destination_busy", "Number of Destination Busy SIP/H323 calls"),
        3:  ("sip_no_answer", "Number of No Answer SIP/H323 calls"),
        4:  ("sip_no_route", "Number of No Route SIP/H323 calls. Most likely to be due to wrong number"),
        5:  ("sip_no_capability", "Number of No capability match between peers on SIP/H323 calls"),
        6:  ("sip_failed", "Number of failed SIP/H323 calls"),
        7:  ("sip_fax_attempted", "Number of Attempted SIP/H323 fax calls"),
        8:  ("sip_fax_success", "Number of SIP/H323 fax success calls"),
        9:  ("sip_total_duration", "total duration of SIP/H323 calls"),
        }
    if len(info) == 2:
        # Tel2IP
        this_time = time.time()
        for key, value in enumerate(info[0][0]):
            if key == 9:
                yield 0, "Tel2IP %s: %d" % (sipperf_info[key][1], saveint(value)), [ ( 'tel2ip_%s' % sipperf_info[key][0], saveint(value) ) ]
            else:
                rate = get_rate('acgateway_sipperf.tel2ip_%s' % sipperf_info[key][0], this_time, saveint(value))
                yield 0, "Tel2IP %s: %0.1f/s" % (sipperf_info[key][1], rate), [ ( 'tel2ip_%s' % sipperf_info[key][0], rate ) ]
        # IP2Tel
        for key, value in enumerate(info[1][0]):
            if key == 9:
                yield 0, "IP2Tel %s: %d" % (sipperf_info[key][1], saveint(value)), [ ( 'ip2tel_%s' % sipperf_info[key][0], saveint(value) ) ]
            else:
                rate = get_rate('acgateway_sipperf.ip2tel_%s' % sipperf_info[key][0], this_time, saveint(value))
                yield 0, "IP2Tel %s: %0.1f/s" % (sipperf_info[key][1], rate), [ ( 'ip2tel_%s' % sipperf_info[key][0], rate ) ]

# check_info['acgateway_sipperf'] = {
#     'inventory_function'    : inventory_acgateway_sipperf,
#     'check_function'        : check_acgateway_sipperf,
#     'service_description'   : 'SIP Performance',
#     'has_perfdata'          : True,
#     'snmp_info'             : [ ( '.1.3.6.1.4.1.5003.10.3.1.1.1', [
#         '1.0',  # AcPerfH323SIPGateway::acPerfTel2IPAttemptedCalls
#         '2.0',  # AcPerfH323SIPGateway::acPerfTel2IPEstablishedCalls
#         '3.0',  # AcPerfH323SIPGateway::acPerfTel2IPBusyCalls
#         '4.0',  # AcPerfH323SIPGateway::acPerfTel2IPNoAnswerCalls
#         '5.0',  # AcPerfH323SIPGateway::acPerfTel2IPNoRouteCalls
#         '6.0',  # AcPerfH323SIPGateway::acPerfTel2IPNoMatchCalls
#         '7.0',  # AcPerfH323SIPGateway::acPerfTel2IPFailCalls
#         '8.0',  # AcPerfH323SIPGateway::acPerfTel2IPFaxAttemptedCalls
#         '9.0',  # AcPerfH323SIPGateway::acPerfTel2IPFaxSuccessCalls
#         '10.0', # AcPerfH323SIPGateway::acPerfTel2IPTotalDuration
#         ] ),
#                                 ( '.1.3.6.1.4.1.5003.10.3.1.1.2', [
#         '1.0',  # AcPerfH323SIPGateway::acPerfIP2TelAttemptedCalls
#         '2.0',  # AcPerfH323SIPGateway::acPerfIP2TelEstablishedCalls
#         '3.0',  # AcPerfH323SIPGateway::acPerfIP2TelBusyCalls
#         '4.0',  # AcPerfH323SIPGateway::acPerfIP2TelNoAnswerCalls
#         '5.0',  # AcPerfH323SIPGateway::acPerfIP2TelNoRouteCalls
#         '6.0',  # AcPerfH323SIPGateway::acPerfIP2TelNoMatchCalls
#         '7.0',  # AcPerfH323SIPGateway::acPerfIP2TelFailCalls
#         '8.0',  # AcPerfH323SIPGateway::acPerfIP2TelFaxAttemptedCalls
#         '9.0',  # AcPerfH323SIPGateway::acPerfIP2TelFaxSuccessCalls
#         '10.0', # AcPerfH323SIPGateway::acPerfIP2TelTotalDuration
#     ] ) ],
#     'snmp_scan_function'    : lambda oid: oid('.1.3.6.1.2.1.1.2.0').startswith('.1.3.6.1.4.1.5003.8.1.1'),
# }
