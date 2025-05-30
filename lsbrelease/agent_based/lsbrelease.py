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

from collections.abc import Mapping # type: ignore
from typing import Any # type: ignore

from cmk.agent_based.v2 import (
    AgentSection,
    check_levels,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    HostLabel,
    HostLabelGenerator,
    Metric,
    Result,
    Service,
    State,
    StringTable,
)

from cmk.utils import debug
from pprint import pprint # type: ignore

Section = Mapping[str, Any]

def parse_lsbrelease(string_table: StringTable) -> Section:
    lsbinfo = {}
    for line in string_table:
        try:
            key, value = (" ".join(line)).split(': ')
            lsbinfo[key] = value
        except ValueError:
            pass
    return lsbinfo

# def parse_lnx_distro(info: StringTable) -> Section:
#     parsed = {}
#     filename = None
#     for line in info:
#         if line[0].startswith("[[[") and line[0].endswith("]]]"):
#             filename = line[0][3:-3]
#             parsed[filename] = {}
#         elif filename is not None:
#             for entry in line:
#                 if entry.count('=') == 0:
#                     continue
#                 k, v = [x.replace('"', '') for x in entry.split("=", 1)]
#                 parsed[filename][k] = v
#     return parsed

def versiontuple(v):
    return tuple(map(int, [item for sublist in map(lambda x: x.split('-'), v.split('.')) for item in sublist]))

def host_label_lsbrelease(section: Section) -> HostLabelGenerator:
    if section:
        infomap = {
            'Codename': 'lsbrelease/codename',
            'Distributor ID': 'lsbrelease/distribution',
            'Release': 'lsbrelease/version',
            }
        for k, v in infomap.items():
            if k in section:
                yield HostLabel(v, section[k].lower())

agent_section_lsbrelease = AgentSection(
    name="lsbrelease",
    parse_function=parse_lsbrelease,
    host_label_function=host_label_lsbrelease,
)

def discovery_lsbrelease(section: Section) -> DiscoveryResult:
    if section:
        yield Service()

def check_lsbrelease(params, section: Section) -> CheckResult:
    if debug.enabled():
        print(f"params: {params}")
        print(f"section: {section}")
    desc = section.get('Description')
    found = False
    if desc:
        for distinfo in params.get('distributions', []):
            distribution = distinfo["name"]
            version = distinfo["version"]
            if desc.lower().startswith(distribution.lower()):
                yield Result(state=State.OK, summary=desc)
                current_version=(0, 0)
                release = section.get('Release')
                if release:
                    current_version = versiontuple(release)
                    if release not in desc:
                        yield Result(state=State.OK, summary="Release " + release)
                test_version = versiontuple(version)
                if current_version[0] < test_version[0]:
                    yield Result(state=State.CRIT,
                                 summary="expected at least version %d" % test_version[0])
                elif current_version < test_version:
                    yield Result(state=State.WARN,
                                 summary="expected version %s" % version)
                found = True
                break
    if not found:
        yield Result(state=State.UNKNOWN,
                     summary="Unknown Distribution: %s" % desc)

check_plugin_lsbrelease = CheckPlugin(
    name="lsbrelease",
    service_name="Distribution Release",
    sections=["lsbrelease"],
    discovery_function=discovery_lsbrelease,
    check_function=check_lsbrelease,
    check_default_parameters={
        'distributions': [
            {'name': 'CentOS Stream', 'version': '9'},
            {'name': 'Debian', 'version': '11'},
            {'name': 'openSUSE', 'version': '15.6'},
            {'name': 'SUSE EOL', 'version': '99'},
            {'name': 'SUSE Linux Enterprise Server', 'version': '15.6'},
            {'name': 'Ubuntu', 'version': '24.04'},
        ],
    },
    check_ruleset_name="lsbrelease",
)
