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

from collections.abc import Mapping # type: ignore
from typing import Any # type: ignore

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    get_rate,
    get_value_store,
    Metric,
    Result,
    Service,
    State,
    StringTable,
)

import time

Section = Mapping[str, Any]

def parse_rspamd(string_table: StringTable) -> Section:
    import json
    import re
    try:
        raw = " ".join([item for sublist in string_table for item in sublist])
        # rspamd kann nan/inf Werte ausgeben, die kein gültiges JSON sind
        raw = re.sub(r'\b(nan|inf)\b', 'null', raw)
        return json.loads(raw)
    except ValueError:
        return {}

agent_section_rspamd = AgentSection(
    name="rspamd",
    parse_function=parse_rspamd,
)

def discover_rspamd(section: Section) -> DiscoveryResult:
    if 'scanned' in section:
        yield Service()

def check_rspamd(section: Section) -> CheckResult:
    data = {
        'scanned': 0,
        'ham_count': 0,
        'spam_count': 0,
        'actions': {
            'add header': 0,
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
        yield Result(
            state=State.UNKNOWN,
            summary="No data received",
        )
    else:
        value_store = get_value_store()
        for key, value in data.items():
            if type(value) == int:
                if key in section:
                    data[key] = section[key]
                    rate[key] = get_rate(
                        value_store,
                        'rspamd.%s' % key,
                        now,
                        data[key],
                    )
                else:
                    rate[key] = 0.0
            elif type(value) == dict:
                if key not in rate:
                    rate[key] = {}
                for key2, value2 in data[key].items():
                    if type(value2) == int:
                        if key in section and key2 in section[key]:
                            data[key][key2] = section[key][key2]
                            rate[key][key2] = get_rate(
                                value_store,
                                'rspamd.%s.%s' % (key, key2),
                                now,
                                data[key][key2],
                            )
                        else:
                            rate[key][key2] = 0.0

        total = data['scanned']
        # total_rate = rate['scanned']

        for key, value in data.items():
            if type(value) == int:
                perc = 0
                if total > 0:
                    perc = value*100.0/total
                yield Result(
                    state=State.OK,
                    summary='%d %s (%0.2f%%)' % (value, key, perc),
                )
                yield Metric('rspamd_%s_rate' % key, rate[key])
            elif type(value) == dict:
                for key2, value2 in data[key].items():
                    if type(value2) == int:
                        perc = 0
                        if total > 0:
                            perc = value2*100.0/total
                        yield Result(
                            state=State.OK,
                            summary='%d %s (%0.2f%%)' % (value2, key2, perc),
                        )
                        yield Metric('rspamd_%s_%s_rate' % (key, key2.replace(' ', '_')), rate[key][key2])

check_plugin_rspamd = CheckPlugin(
    name="rspamd",
    service_name="Rspamd",
    sections=["rspamd"],
    discovery_function=discover_rspamd,
    check_function=check_rspamd,
)