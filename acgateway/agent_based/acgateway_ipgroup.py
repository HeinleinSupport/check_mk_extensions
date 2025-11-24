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

from .agent_based_api.v1 import (
    all_of,
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

def _item_acgateway_ipgroup(line):
    return "%s %s" % (line[0], line[4])

def parse_acgateway_ipgroup(string_table):
    rowStatus = {
        '1': 'active',
        '2': 'notInService',
        '3': 'notReady',
    }
    ipGroupType = {
        '0': 'server',
        '1': 'user',
        '2': 'gateway',
    }
    section = {}
    for line in string_table:
        item = _item_acgateway_ipgroup(line)
        section[item] = {
            'ipgroupstatus': rowStatus.get(line[1], 'unknown'),
            'ipgrouptype': ipGroupType.get(line[2], 'unknown'),
            'description': line[3],
            'name': line[4]
        }
    return section

register.snmp_section(
    name="acgateway_ipgroup",
    detect=all_of(
        contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.5003.8.1.1"),
        contains(".1.3.6.1.2.1.1.1.0", "SW Version: 7.20A"),
    ),
    parse_function=parse_acgateway_ipgroup,
    fetch=SNMPTree(
        base='.1.3.6.1.4.1.5003.9.10.3.1.1.23.21.1',
        oids=[
            '1',  # 0  AcGateway::ipGroupIndex
            '2',  # 1  AcGateway::ipGroupRowStatus
            '5',  # 2  AcGateway::ipGroupType
            '6',  # 3  AcGateway::ipGroupDescription
            '31', # 4  AcGateway::ipGroupName
        ]),
)

def discover_acgateway_ipgroup(section):
    for item, data in section.items():
        yield Service(item=item, parameters={'ipgroupstatus': data.get('ipgroupstatus')})

def check_acgateway_ipgroup(item, params, section):
    if item in section:
        data = section[item]
        yield Result(state=State.OK,
                     summary='ip group type: %s' % data['ipgrouptype'])
        if data['description']:
            yield Result(state=State.OK,
                         summary=data['description'])
        for param, value in params.items():
            if value != data.get(param):
                yield Result(state=State.CRIT,
                             summary='%s is %s' % (param, data.get(param)))

register.check_plugin(
    name="acgateway_ipgroup",
    service_name="IP Group %s",
    discovery_function=discover_acgateway_ipgroup,
    check_function=check_acgateway_ipgroup,
    check_default_parameters={},
)
