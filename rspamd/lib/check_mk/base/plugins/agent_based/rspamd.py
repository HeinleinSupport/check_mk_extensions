#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2018 Heinlein Support GmbH
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

from .agent_based_api.v1 import (
    get_rate,
    get_value_store,
    register,
    Metric,
    Result,
    ServiceLabel,
    Service,
    State,
)

import time

def parse_rspamd(string_table):
    import json
    try:
        return json.loads(" ".join([item for sublist in string_table for item in sublist]))
    except ValueError:
        return {}

register.agent_section(
    name="rspamd",
    parse_function=parse_rspamd,
)

def discover_rspamd(section):
    if 'scanned' in section:
        yield Service()

def check_rspamd(params, section):
    data = { 'scanned': 0,
             'ham_count': 0,
             'spam_count': 0,
             'actions': { 'add header': 0,
                          'greylist': 0,
                          'no action': 0,
                          'reject': 0,
                          'rewrite subject': 0,
                          'soft reject': 0,
                          },
            }
    rate = {}
    now = time.time()

    if 'scanned' not in section:
        yield Result(state=State.UNKNOWN,
                     summary="No data received")
    else:
        value_store = get_value_store()
        for key, value in data.items():
            if type(value) == int:
                if key in section:
                    data[key] = section[key]
                    rate[key] = get_rate(value_store,
                                         'rspamd.%s' % key,
                                         now,
                                         data[key])
                else:
                    rate[key] = 0.0
            elif type(value) == dict:
                if key not in rate:
                    rate[key] = {}
                for key2, value2 in data[key].items():
                    if type(value2) == int:
                        if key2 in section[key]:
                            data[key][key2] = section[key][key2]
                            rate[key][key2] = get_rate(value_store,
                                                       'rspamd.%s.%s' % (key, key2),
                                                       now,
                                                       data[key][key2])
                        else:
                            rate[key][key2] = 0.0

        total = data['scanned']
        total_rate = rate['scanned']

        for key, value in data.items():
            if type(value) == int:
                perc = 0
                if total > 0:
                    perc = value*100.0/total
                yield Result(state=State.OK,
                             summary='%d %s (%0.2f%%)' % (value, key, perc))
                yield Metric('rspamd_%s_rate' % key, rate[key])
            elif type(value) == dict:
                for key2, value2 in data[key].items():
                    if type(value2) == int:
                        perc = 0
                        if total > 0:
                            perc = value2*100.0/total
                        yield Result(state=State.OK,
                                     summary='%d %s (%0.2f%%)' % (value2, key2, perc))
                        yield Metric('rspamd_%s_%s_rate' % (key, key2.replace(' ', '_')), rate[key][key2])

register.check_plugin(
    name="rspamd",
    service_name="Rspamd",
    sections=["rspamd"],
    discovery_function=discover_rspamd,
    # discovery_default_parameters={},
    # discovery_ruleset_name="",
    # discovery_ruleset_type=register.RuleSetType.MERGED,
    check_function=check_rspamd,
    check_default_parameters={},
    check_ruleset_name="rspamd",
)
