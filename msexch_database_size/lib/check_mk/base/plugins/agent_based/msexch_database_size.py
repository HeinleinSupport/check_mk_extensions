#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 vim: set ft=python:-*-

# (c) 2020 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>

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

# {'DatabaseSize': '3.625 GB (3,892,314,112 bytes)', 'Name': 'deactivated_Users'}
# {'DatabaseSize': '1.003 TB (1,102,732,853,248 bytes)', 'Name': 'active_Users'}
# {'DatabaseSize': '41.63 GB (44,694,503,424 bytes)', 'Name': 'Shared_Mailbox'}

# info = [[u'"Name"', u'"DatabaseSize"'],
#         [u'"deactivated_Users"', u'"3.625 GB (3,892,314,112 bytes)"'],
#         [u'"active_Users"', u'"1.003 TB (1,102,732,853,248 bytes)"'],
#         [u'"Shared_Mailbox"', u'"41.63 GB (44,694,503,424 bytes)"']]

from .agent_based_api.v1.type_defs import (
    CheckResult,
    DiscoveryResult,
)

from .agent_based_api.v1 import (
    check_levels,
    register,
    render,
    Service,
    )

def parse_msexch_database_size(string_table):
    section = {}
    for line in string_table:
        values = {}
        name = line[0].strip('"')
        if name == u'Name':
            continue
        sizestr = line[1].strip('"')
        size = int(sizestr.split('(')[1].split(' ')[0].replace(',', ''))
        values['size'] = size
        if len(line) > 2:
            availspacestr = line[2].strip('"')
            availableSpace = int(availspacestr.split('(')[1].split(' ')[0].replace(',', ''))
            values['availSpace'] = availableSpace
        section[name] = values

    return section

register.agent_section(
    name="msexch_database_size",
    parse_function=parse_msexch_database_size,
)

def discover_msexch_database_size(section) -> DiscoveryResult:
    for instance, data in section.items():
        yield Service(item=instance)

def check_msexch_database_size(item, params, section) -> CheckResult:
    values = section.get(item)
    if values is None:
        return

    yield from check_levels(values['size'],
                            metric_name='database_size',
                            levels_upper=params['size'],
                            render_func=render.disksize,
                            label="Size")

    if 'availSpace' in values:
        availSpacePct = values['availSpace'] * 100 / values['size']
        yield from check_levels(availSpacePct,
                                metric_name='availableNewMailboxSpace',
                                levels_upper=params['availSpace'],
                                render_func=render.percent,
                                label="Available New Mailbox Space (pct)")

register.check_plugin(
    name="msexch_database_size",
    service_name="Exchange Database Size %s",
    sections=["msexch_database_size"],
    discovery_function=discover_msexch_database_size,
    check_function=check_msexch_database_size,
    check_default_parameters={
        'size': None,
         'availSpace': (20.0,40.0)
         },
    check_ruleset_name="msexch_database_size",
)
