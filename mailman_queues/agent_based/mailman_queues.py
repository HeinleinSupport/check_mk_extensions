#!/usr/bin/env python
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

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    Metric,
    State,
    Service,
)

def mailman_queues_name(line):
    return line[0]

def parse_mailman_queues(string_table):
    section = {}
    for line in string_table:
        section[mailman_queues_name(line)] = { 'mails': int(line[3]),
                                               'bytes': int(line[4]),
        }
    return section

agent_section_mailman_queues = AgentSection(
    name="mailman_queues",
    parse_function=parse_mailman_queues,
)

def discover_mailman_queues(section) -> DiscoveryResult:
    for queue in section:
        yield Service(item=queue)

def check_mailman_queues(item, section) -> CheckResult:
    if item in section:
        mails = section[item]['mails']
        bytes = section[item]['bytes']
        rc = State.OK
        yield Result(state=rc,
                     summary="%d mails" % mails)
        yield Metric("length", mails)
        yield Metric("size", bytes)

check_plugin_mailman_queues = CheckPlugin(
    name="mailman_queues",
    service_name="Mailman Queue %s",
    sections=["mailman_queues"],
    discovery_function=discover_mailman_queues,
    check_function=check_mailman_queues,
)
