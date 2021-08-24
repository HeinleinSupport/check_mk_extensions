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

from .agent_based_api.v1.type_defs import (
    CheckResult,
    DiscoveryResult,
    HostLabelGenerator,
)

from .agent_based_api.v1 import (
    register,
    Result,
    State,
    HostLabel,
    Service,
    )

def parse_lsbrelease(string_table):
    lsbinfo = {}
    for line in string_table:
        key, value = (" ".join(line)).split(': ')
        lsbinfo[key] = value
    return lsbinfo

def parse_lnx_distro(info):
    parsed = {}
    filename = None
    for line in info:
        if line[0].startswith("[[[") and line[0].endswith("]]]"):
            filename = line[0][3:-3]
            parsed[filename] = {}
        elif filename is not None:
            for entry in line:
                if entry.count('=') == 0:
                    continue
                k, v = [x.replace('"', '') for x in entry.split("=", 1)]
                parsed[filename][k] = v
    return parsed

def versiontuple(v):
    return tuple(map(int, [item for sublist in map(lambda x: x.split('-'), v.split('.')) for item in sublist]))

def host_label_lsbrelease(section) -> HostLabelGenerator:
    if section:
        infomap = {
            'Codename': 'lsbrelease/codename',
            'Distributor ID': 'lsbrelease/distribution',
            'Release': 'lsbrelease/version',
            }
        for k, v in infomap.items():
            if k in section:
                yield HostLabel(v, section[k])

register.agent_section(
    name="lsbrelease",
    parse_function=parse_lsbrelease,
    host_label_function=host_label_lsbrelease,
)

def discovery_lsbrelease(section) -> DiscoveryResult:
    if section:
        yield Service()

def check_lsbrelease(params, section) -> CheckResult:
    desc = section.get('Description')
    found = False
    if desc:
        for distribution, version in params.get('distributions', []):
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
                if current_version < test_version:
                    yield Result(state=State.WARN,
                                 summary="expected version %s" % version)
                found = True
                break
    if not found:
        yield Result(state=State.UNKNOWN,
                     summary="Unknown Distribution: %s" % desc)

register.check_plugin(
    name="lsbrelease",
    service_name="Distribution Release",
    sections=["lsbrelease"],
    discovery_function=discovery_lsbrelease,
    check_function=check_lsbrelease,
    check_default_parameters={'distributions': [
        ( 'CentOS', '7' ),
        ( 'Debian', '9.9' ),
        ( 'openSUSE', '15.1'),
        ( 'SUSE EOL', '99' ),
        ( 'SUSE Linux Enterprise Server', '12.5' ),
        ( 'Ubuntu', '16.04.7'),
    ]},
    check_ruleset_name="lsbrelease",
)
