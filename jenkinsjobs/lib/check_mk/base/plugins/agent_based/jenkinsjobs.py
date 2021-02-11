#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2019 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>
#

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
    check_levels,
    check_levels_predictive,
    get_rate,
    get_value_store,
    register,
    render,
    Metric,
    Result,
    State,
    Service,
    )

import json
import time

def parse_jenkinsjobs(string_table):
    section = {}
    for line in string_table:
        section.update(json.loads(line[0]))
    return section

register.agent_section(
    name="jenkinsjobs",
    parse_function=parse_jenkinsjobs,
)

def discover_jenkinsjobs(section) -> DiscoveryResult:
    for name, job in section.items():
        if job['data'].get('buildable', False):
            yield Service(item=name)

def check_jenkinsjobs(item, section) -> CheckResult:
    if item in section:
        job = section[item]['data']

        yield Result(state=State.OK,
                     summary=job['displayName'])

        if 'url' in section[item]:
            yield Result(state=State.OK,
                         summary="URL: %s " % section[item]['url'])

        lastUnsuccessfulBuild = job.get('lastUnsuccessfulBuild', {'number': 0})
        if not lastUnsuccessfulBuild:
            lastUnsuccessfulBuild = {'number': 0}
        lastUnsuccessfulBuild = lastUnsuccessfulBuild.get('number', 0)
        lastStableBuild = job.get('lastStableBuild', {'number': 0})
        if not lastStableBuild:
            lastStableBuild = {'number': 0}
        lastStableBuild = lastStableBuild.get('number', 0)
        numFailedBuilds = 0
        if lastUnsuccessfulBuild > 0:
            numFailedBuilds = lastUnsuccessfulBuild - lastStableBuild
        if numFailedBuilds > 0:
            yield Result(state=State.WARN,
                         summary="%d failed builds" % numFailedBuilds)

        lastCompletedBuild = job.get('lastCompletedBuild', {'data': None}).get('data', {})
        if lastCompletedBuild:
            yield Result(state=State.OK,
                         notice="last complete build started at %s" % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(lastCompletedBuild['timestamp']/1000.0)))
            yield Result(state=State.OK,
                         notice="completed at %s" % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime((lastCompletedBuild['timestamp']+lastCompletedBuild['duration'])/1000.0)))
            if lastCompletedBuild.get('result') != u'SUCCESS':
                yield Result(state=State.CRIT,
                             summary=lastCompletedBuild.get('result'))
            art = lastCompletedBuild.get('artifacts', {})
            checkmkart = art.get('checkmk.txt', {})
            for error in checkmkart.get('error', []):
                yield Result(state=State.CRIT,
                             summary=error)
            for metric, value in checkmkart.get('perfdata', {}).items():
                yield Metric(metric, value)
        else:
            yield Result(state=State.WARN,
                         summary="no completed build")

register.check_plugin(
    name="jenkinsjobs",
    service_name="JenkinsJob %s",
    sections=["jenkinsjobs"],
    discovery_function=discover_jenkinsjobs,
    check_function=check_jenkinsjobs,
)
