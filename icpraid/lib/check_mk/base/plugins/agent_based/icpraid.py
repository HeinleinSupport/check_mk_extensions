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

from .agent_based_api.v1.type_defs import (
    CheckResult,
    DiscoveryResult,
)

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

def versiontuple(v):
    return tuple(map(int, (v.split("."))))

def parse_icpraid(string_table):
    ctid = -1
    data = {}
    inController = False
    inLogicalDevice = False
    inChannel = False
    inPhysicalDevice = False
    for line in string_table:
        completeLine = ' '.join(line)
        if completeLine == 'Controller information':
            inController = True
            ctid += 1
            data[ctid] = { 'info': {}, 'ld': {}, 'ch': {} }
            continue
        if ' '.join(line[:-1]) == 'Logical device number':
            inController = False
            inLogicalDevice = True
            ldid = int(line[-1])
            data[ctid]['ld'][ldid] = {}
            continue
        if completeLine[:9] == 'Channel #':
            inLogicalDevice = False
            inPhysicalDevice = False
            inChannel = True
            chid = int(completeLine[9:-1])
            data[ctid]['ch'][chid] = {'info': {}, 'pd': {}}
            continue
        if completeLine[:8] == 'Device #':
            inChannel = False
            inPhysicalDevice = True
            pdid = int(completeLine[8:])
            data[ctid]['ch'][chid]['pd'][pdid] = {}
            continue
        if ':' in line:
            idx = line.index(':')
            if idx:
                key = ' '.join(line[:idx])
                value = ' '.join(line[idx+1:])
                if inController:
                    data[ctid]['info'][key] = value
                if inLogicalDevice:
                    data[ctid]['ld'][ldid][key] = value
                if inChannel:
                    data[ctid]['ch'][chid]['info'][key] = value
                if inPhysicalDevice:
                    data[ctid]['ch'][chid]['pd'][pdid][key] = value
    return data

register.agent_section(
    name="icpraid",
    parse_function=parse_icpraid,
)

def discover_icpraid(section) -> DiscoveryResult:
    for ctid in section.keys():
        yield Service(item='Controller %d' % ctid)
        for ldid in section[ctid]['ld'].keys():
            yield Service(item='LD %d:%d' % (ctid, ldid))
        for chid in section[ctid]['ch'].keys():
            for pdid in section[ctid]['ch'][chid]['pd'].keys():
                yield Service(item='PD: %d:%d:%d' % (ctid, chid, pdid))

def check_icpraid(item, section) -> CheckResult:
    if item[:10] == 'Controller':
        ctid = int(item[11:])
        if ctid in section:
            for key, value in section[ctid]['info'].items():
                rc = State.OK
                if key == 'Defunct disk drive count':
                    if int(value) > 0:
                        rc = State.WARN
                if key == 'Controller Status':
                    if value != 'Optimal':
                        rc = State.CRIT
                if key == 'Status':
                    # ignore Battery Status for now
                    continue
                yield Result(state=rc,
                             notice=key + ": " + value)
    if item[:2] == 'LD':
        ctid, ldid = map(int, item[3:].split(':'))
        if ctid in section:
            if ldid in section[ctid]['ld']:
                for key, value in section[ctid]['ld'][ldid].items():
                    rc = State.OK
                    if key == 'Status of logical device':
                        if value != 'Optimal':
                            rc = State.CRIT
                    yield Result(state=rc,
                                 notice=key + ": " + value)
    if item[:2] == 'PD':
        ctid, chid, pdid = map(int, item[3:].split(':'))
        if ctid in section:
            if chid in section[ctid]['ch']:
                if pdid in section[ctid]['ch'][chid]['pd']:
                    for key, value in section[ctid]['ch'][chid]['pd'][pdid].items():
                        rc = State.OK
                        if key == 'State':
                            if value != 'Online':
                                rc = State.CRIT
                        if key == 'Temperature status':
                            if value != 'Normal':
                                rc = State.CRIT
                        yield Result(state=rc,
                                     notice=key + ": " + value)

register.check_plugin(
    name="icpraid",
    service_name="ICP RAID %s",
    sections=["icpraid"],
    discovery_function=discover_icpraid,
    check_function=check_icpraid,
)
