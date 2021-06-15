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

# .1.3.6.1.4.1.1369.6.1.1.4.0 2 --> STONESOFT-NETNODE-MIB::nodeCPULoad.0

from .agent_based_api.v1 import (
    contains,
    get_value_store,
    register,
    render,
    Result,
    Service,
    SNMPTree,
    State,
)
from .utils.cpu_util import check_cpu_util
import time

def parse_stonesoft_firewall_cpu(string_table):
    return string_table

register.snmp_section(
    name="stonesoft_firewall_cpu",
    detect=contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.1369.5.2"),
    parse_function=parse_stonesoft_firewall_cpu,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.1369.6.1.1",
        oids=["4.0"]
    ),
)

def discover_stonesoft_firewall_cpu(section):
    yield Service()

def check_stonesoft_firewall_cpu(params, section):
    num_cpus = 0
    util = 0.0
    cores = []
    for line in section:
        core_util = float(line[0])
        cores.append(("core%d" % num_cpus, core_util))
        util += core_util
        num_cpus += 1
    if num_cpus > 0:
        util = util / num_cpus
        vs = get_value_store()
        yield from check_cpu_util(
            util=util,
            params=params,
            cores=cores,
            value_store=vs,
            this_time=time.time(),
        )

register.check_plugin(
    name='stonesoft_firewall_cpu',
    service_name="CPU utilization",
    discovery_function=discover_stonesoft_firewall_cpu,
    check_function=check_stonesoft_firewall_cpu,
    check_ruleset_name='cpu_utilization_os',
    check_default_parameters={
        "levels": (80.0, 90.0),
    },
)
