#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#     2021 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>

# +-----------------------------------------------------------------+
# |                                                                 |
# |        (  ___ \     | \    /\|\     /||\     /|( (    /|        |
# |        | (   ) )    |  \  / /| )   ( || )   ( ||  \  ( |        |
# |        | (__/ /     |  (_/ / | |   | || (___) ||   \ | |        |
# |        |  __ (      |   _ (  | |   | ||  ___  || (\ \) |        |
# |        | (  \ \     |  ( \ \ | |   | || (   ) || | \   |        |
# |        | )___) )_   |  /  \ \| (___) || )   ( || )  \  |        |
# |        |/ \___/(_)  |_/    \/(_______)|/     \||/    )_)        |
# |                                                                 |
# | Copyright Bastian Kuhn 2011                mail@bastian-kuhn.de | 
# +-----------------------------------------------------------------+
#
# This file is a check Script for check_mk
# Information about me can be found at http://bastian-kuhn.de
# Information about check_mk at http://mathias-kettner.de/check_mk.
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


# Example Agent Output
#<<<dir_size>>>
#17516   /tmp/
#626088  /usr/local/

from .agent_based_api.v1 import (
    check_levels,
    register,
    render,
    Result,
    Metric,
    State,
    ServiceLabel,
    Service,
)

def parse_dir_size(string_table):
    section = {}
    for line in string_table:
        size = int(line[0])
        path = ' '.join(line[1:])
        section[path] = size * 1024
    return section

register.agent_section(
    name="dir_size",
    parse_function=parse_dir_size,
)

def discover_dir_size(section):
    for path in section:
        yield Service(item=path)

def check_dir_size(item, params, section):
    if item in section:
        factor = 1
        if 'unit' in params:
            unit = params['unit']

            dir_size_factor = {
                'B': 1,
                'KB': 1024,
                'MB': 1048576,
                'GB': 1073741824,
                'TB': 1099511627776,
            }

            factor = dir_size_factor.get(unit)
            
        warn = params.get('warn')
        crit = params.get('crit')

        if warn and factor:
            warn *= factor
        if crit and factor:
            crit *= factor
        if warn or crit:
            params._data['levels_upper'] = (warn, crit)

        yield from check_levels(
            section[item],
            levels_upper=params.get('levels_upper'),
            metric_name="dir_size",
            label="Folder size",
            render_func=render.bytes,
        )

register.check_plugin(
    name="dir_size",
    service_name="Size of %s",
    sections=["dir_size"],
    discovery_function=discover_dir_size,
    # discovery_default_parameters={},
    # discovery_ruleset_name="",
    # discovery_ruleset_type=register.RuleSetType.MERGED,
    check_function=check_dir_size,
    check_default_parameters={
        'unit': 'KB',
    },
    check_ruleset_name="dir_size",
)
