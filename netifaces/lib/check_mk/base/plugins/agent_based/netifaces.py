#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2013 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  This file is distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

from .agent_based_api.v1.type_defs import (
    CheckResult,
    DiscoveryResult,
    HostLabelGenerator,
)

from .agent_based_api.v1 import (
    check_levels,
    register,
    Result,
    State,
    HostLabel,
    Service,
    )

from functools import reduce
import socket
import dns.reversename
import ipaddress

def discovery_netifaces_rbl(params, section) -> DiscoveryResult:
    if_table, ip_stats = section
    if params.get('active'):
        include_list = list(map(ipaddress.ip_network, params.get('include', [])))
        exclude_list = list(map(ipaddress.ip_network, params.get('exclude', [])))
        for iface, info in ip_stats.items():
            for addr in map(lambda x: x.split('/')[0], info.inet + info.inet6):
                a = ipaddress.ip_address(addr)
                if reduce(lambda result, network: result or (a in network), include_list, False):
                    yield Service(item=addr)
                    continue
                if not reduce(lambda result, network: result or (a in network), exclude_list, False):
                    yield Service(item=addr)

def check_netifaces_rbl(item, params, section) -> CheckResult:
    levels = { 'warn': State.WARN,
               'crit': State.CRIT }
    reverse_domain = { 'inet': dns.reversename.ipv4_reverse_domain,
                       'inet6': dns.reversename.ipv6_reverse_domain,
                     }
    if_table, ip_stats = section
    for iface, info in ip_stats.items():
        for family in ["inet", "inet6"]:
            for addr in map(lambda x: x.split('/')[0], getattr(info, family)):
                if item == addr:
                    yield Result(state=State.OK,
                                 summary="bound on %s" % iface)
                    count = 0
                    for level, levelres in levels.items():
                        for rbl in params.get(level, []):
                            ptr = "%s.%s." % (dns.reversename.from_address(addr) - reverse_domain[family], rbl)
                            try:
                                ip = socket.gethostbyname(ptr)
                                count += 1
                                yield Result(state=levelres,
                                             notice='found in %s: %s' % (rbl, ip))
                            except socket.gaierror as er:
                                if er.args[0] == socket.EAI_NONAME:
                                    yield Result(state=State.OK,
                                                 notice='not found in %s' % rbl)
                                else:
                                    yield Result(state=State.WARN,
                                                 notice='%s yields %s' % (rbl, er))
                    if count > 1:
                        yield Result(state=State.CRIT,
                                     summary='found in more than 1 RBL')

register.check_plugin(
    name="netifaces_rbl",
    service_name="RBL %s",
    sections=["lnx_if"],
    discovery_function=discovery_netifaces_rbl,
    discovery_ruleset_name="discovery_rbl_rules",
    discovery_default_parameters={
        'active': False,
        'include': [],
        'exclude': [
            '10.0.0.0/8',
            '127.0.0.0/8',
            '172.16.0.0/12',
            '192.168.0.0/16',
            '::1/128',
            'fe80::/10',
            'fc00::/7',
        ],
    },
    check_function=check_netifaces_rbl,
    check_default_parameters={
        'crit': [ "bl.spamcop.org", "zen.spamhaus.org", "ix.dnsbl.manitu.net" ]
    },
    check_ruleset_name="netifaces_rbl",
)
