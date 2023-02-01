#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2017 Heinlein Support GmbH
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
)

from .agent_based_api.v1 import (
    get_value_store,
    register,
    Metric,
    Result,
    State,
    Service,
    )

from .utils import df

import json
import time

def parse_cephosdbluefs(string_table):
    import json
    section = {}
    for line in string_table:
        try:
            section.update(json.loads("".join([item for item in line])))
        except ValueError:
            pass
    return section

register.agent_section(
    name="cephosdbluefs",
    parse_function=parse_cephosdbluefs,
)

def discovery_cephosdbluefs(area, section) -> DiscoveryResult:
    for osdid, perf in section.items():
        if 'bluefs' in perf and perf['bluefs'].get('%s_total_bytes' % area.lower(), 0) > 0:
            yield Service(item="OSD %s %s" % (osdid, area))

def check_cephosdbluefs(area, item, params, section) -> CheckResult:
    for osdid, perf in section.items():
        if item == "OSD %s %s" % (osdid, area) and 'bluefs' in perf:
            value_store = get_value_store()
            size_mb = perf['bluefs'].get('%s_total_bytes' % area.lower(), 0) / 1024.0 / 1024.0
            avail_mb = ( perf['bluefs'].get('%s_total_bytes' % area.lower(), 0) - perf['bluefs'].get('%s_used_bytes' % area.lower(), 0) ) / 1024.0 / 1024.0
            yield from df.df_check_filesystem_single(value_store,
                                                     item,
                                                     size_mb,
                                                     avail_mb,
                                                     0,
                                                     None,
                                                     None,
                                                     params=params)

register.check_plugin(
    name="cephosdbluefs",
    service_name="Ceph %s",
    sections=["cephosdbluefs"],
    discovery_function=lambda section: (yield from discovery_cephosdbluefs('DB', section)),
    check_function=lambda item, params, section: (yield from check_cephosdbluefs('DB', item, params, section)),
    check_default_parameters=df.FILESYSTEM_DEFAULT_PARAMS,
    check_ruleset_name="filesystem",
)

register.check_plugin(
    name="cephosdbluefs_wal",
    service_name="Ceph %s",
    sections=["cephosdbluefs"],
    discovery_function=lambda section: (yield from discovery_cephosdbluefs('WAL', section)),
    check_function=lambda item, params, section: (yield from check_cephosdbluefs('WAL', item, params, section)),
    check_default_parameters=df.FILESYSTEM_DEFAULT_PARAMS,
    check_ruleset_name="filesystem",
)

register.check_plugin(
    name="cephosdbluefs_slow",
    service_name="Ceph %s",
    sections=["cephosdbluefs"],
    discovery_function=lambda section: (yield from discovery_cephosdbluefs('Slow', section)),
    check_function=lambda item, params, section: (yield from check_cephosdbluefs('Slow', item, params, section)),
    check_default_parameters=df.FILESYSTEM_DEFAULT_PARAMS,
    check_ruleset_name="filesystem",
)
