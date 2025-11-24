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

from cmk.base.plugins.agent_based.agent_based_api.v1 import (
    all_of,
    contains,
    register,
    Metric,
    Result,
    Service,
    SNMPTree,
    State,
)


from cmk.utils import debug
from pprint import pprint #type: ignore

def parse_acgateway_users(string_table):
    if debug.enabled():
        pprint(string_table)
    section = None
    if len(string_table) == 1:
        for tx_trans, rx_trans, users in string_table:
            section = {
                'tx_trans': int(tx_trans),
                'rx_trans': int(rx_trans),
                'users': int(users),
            }
    if debug.enabled():
        pprint(section)
    return section

register.snmp_section(
    name="acgateway_users",
    detect=all_of(
        contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.5003.8.1.1"),
        contains(".1.3.6.1.2.1.1.1.0", "SW Version: 7.20A"),
    ),
    parse_function=parse_acgateway_users,
    fetch=SNMPTree(
        base='.1.3.6.1.4.1.5003.10.8.2',
        oids=[
            "52.41.1.3.0.0", # AC-PM-Control-MIB::acPMSIPActiveSIPTransactionsPerSecondVal.tx.0
            "52.41.1.3.1.0", # AC-PM-Control-MIB::acPMSIPActiveSIPTransactionsPerSecondVal.rx.0
            "54.46.1.2.0",   # AC-PM-Control-MIB::acPMSBCRegisteredUsersVal.0
        ]),
)

def discover_acgateway_users(section):
    yield Service()

def check_acgateway_users(section):
    yield Result(state=State.OK,
                 summary="Transactions RX: %d/s" % section['rx_trans'])
    yield Metric('rx_trans', section['rx_trans'])
    yield Result(state=State.OK,
                 summary="Transactions TX: %d/s" % section['tx_trans'])
    yield Metric('tx_trans', section['tx_trans'])
    yield Result(state=State.OK,
                 summary="Registered Users: %d" % section['users'])
    yield Metric('num_user', section['users'])

register.check_plugin(
    name="acgateway_users",
    service_name="SBC Users",
    discovery_function=discover_acgateway_users,
    check_function=check_acgateway_users,
)
