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

# <<<postfix_mailq_details>>>
# active total all 0 4096 /var/spool/postfix/active
# incoming total all 0 4096 /var/spool/postfix/incoming
# deferred total all 0 4096 /var/spool/postfix/deferred
# active age +5 0 0
# incoming age +5 0 0
# deferred age -60 0 0

from .agent_based_api.v1 import (
    register,
    render,
    Result,
    Metric,
    State,
    check_levels,
    ServiceLabel,
    Service,
)

def _postfix_mailq_details_name(line):
    return line[0] + "_" + line[1]

def parse_postfix_mailq_details(string_table):
    section = {}
    for line in string_table:
        item = _postfix_mailq_details_name(line)
        mails = int(line[3])
        try:
            bytes = int(line[4])
        except:
            bytes = 0
        if line[1] == 'age':
            data = (line[2], mails, bytes)
        if line[1] == 'total' and line[2] == 'all':
            data = (line[5], mails, bytes)
        section[item] = data
    return section

register.agent_section(
    name="postfix_mailq_details",
    parse_function=parse_postfix_mailq_details,
)

def discover_postfix_mailq_details(section):
    for queue in section:
        yield Service(item=queue)

def check_postfix_mailq_details(item, params, section):
    if item in section:
        mails = section[item][1]
        bytes = section[item][2]
        if item.endswith('age'):
            if section[item][0][0] == '+':
                label_text = "Mails older than %s minutes" % section[item][0][1:]
            else:
                label_text = "Mails younger than %s minutes" % section[item][0][1:]
        else:
            label_text = "Mails"
        yield Metric("size", bytes)
        yield from check_levels(
            mails,
            levels_upper=params.get('level'),
            metric_name='length',
            label=label_text,
            render_func=lambda x: str(int(x)),
        )

register.check_plugin(
    name="postfix_mailq_details",
    service_name="Postfix Queue %s",
    sections=["postfix_mailq_details"],
    discovery_function=discover_postfix_mailq_details,
    check_function=check_postfix_mailq_details,
    check_default_parameters={
        'level': ( 1000, 1500 ),
    },
    check_ruleset_name="postfix_mailq_details",
)
