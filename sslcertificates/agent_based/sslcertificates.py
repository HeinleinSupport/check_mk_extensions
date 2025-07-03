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

import time
import json
from collections.abc import Mapping # type: ignore
from typing import Any # type: ignore

from cmk.agent_based.v2 import (
    AgentSection,
    check_levels,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    render,
    Result,
    RuleSetType,
    Service,
    ServiceLabel,
    State,
    StringTable,
)

SSLCertificatesSection = Mapping[str, Any]

def parse_sslcertificates(string_table: StringTable) -> SSLCertificatesSection:
    section = {}
    for line in string_table:
        if line[0][0] == '{':
            # new json format for section
            name = False
            data = json.loads(line[0])
            
            if 'file' in data:
                name = data['file']
            if 'thumb' in data:
                name = data['thumb']
            if name and 'subj' in data and 'expires' in data:
                if isinstance(data["subj"], list):
                    data["subj"] = data["subj"][0]
                section[name] = data
        else:
            name = line[0]
            section[name] = {
                'expires': int(line[1])
            }
            algosign = '/'
            if len(line) > 2:
                algosign = line[2]
            if algosign[0] == '/':
                # old agent plugin
                algosign = ''
                subjparts = line[2:]
            else:
                subjparts = line[3:]
            if subjparts[0].startswith('issuer_hash='):
                issuer_hash = subjparts[0][12:]
                subjparts = subjparts[1:]
            else:
                issuer_hash = None
            subject = " ".join(subjparts)

            section[name]['algosign'] = algosign
            section[name]['subj'] = subject
            section[name]['issuer_hash'] = issuer_hash
    return section

agent_section_sslcertificates = AgentSection(
    name="sslcertificates",
    parse_function=parse_sslcertificates,
)


def discover_sslcertificates(params, section: SSLCertificatesSection) -> DiscoveryResult:
    def cleanup_label(value):
        if isinstance(value, str):
            return value.replace(":", "")
        return value

    label_map = {
        'subj': 'sslcertificates/subject',
        'issuer_hash': 'sslcertificates/issuer_hash',
        'issuer': 'sslcertificates/issuer',
        'algosign': 'sslcertificates/algorithm',
        'template': 'sslcertificates/template',
    }

    for name, data in section.items():
        if 'min_lifetime' in params and 'starts' in data:
            if data['expires'] - data['starts'] < params['min_lifetime']:
                continue

        sl = []
        for key, label in label_map.items():
            val = data.get(key)
            if val:
                sl.append(ServiceLabel(label, cleanup_label(val)))
        yield Service(item=name, labels=sl)

def check_sslcertificates(item: str, params, section: SSLCertificatesSection) -> CheckResult:
    warnalgos = params.get('warnalgo', [])
    ignore = params.get('ignore', None)
    
    if item in section:
        data = section[item]
        
        now = int(time.time())
        secondsremaining = data['expires'] - now
        ignored = False

        yield Result(state=State.OK, summary="Subject: %s" % data['subj'])

        if data.get('template'):
            yield Result(state=State.OK, summary="Template: %s" % data['template'])

        if secondsremaining < 0:
            infotext = "expired %s ago on %s" % ( render.timespan(abs(secondsremaining)),
                                                  time.strftime("%c", time.gmtime(data['expires'])))
        else:
            infotext = "expires in %s on %s" % ( render.timespan(secondsremaining),
                                                 time.strftime("%c", time.gmtime(data['expires'])))
        if ignore and -secondsremaining > ignore["after"] * 86400.0:
            yield Result(state=State.OK, summary=infotext + ', ignored because "%s"' % ignore["reason"])
            ignored = True
        else:
            if secondsremaining > 0:
                yield from check_levels(secondsremaining,
                    levels_lower=params.get("age"),
                    metric_name='lifetime_remaining',
                    label='Lifetime Remaining',
                    render_func=render.timespan,
                    )
            else:
                yield from check_levels(secondsremaining,
                    levels_lower=params.get("age"),
                    metric_name='lifetime_remaining',
                    label='Expired',
                    render_func=lambda x: "%s ago" % render.timespan(abs(x)),
                    )

        if data.get('algosign'):
            infotext = "Signature Algorithm: %s" % data['algosign']
            state = State.OK
            if not ignored and data['algosign'] in warnalgos:
                state = State.WARN
            yield Result(state=state, notice=infotext)

check_plugin_sslcertificates = CheckPlugin(
    name="sslcertificates",
    service_name="SSL Certificate in %s",
    sections=["sslcertificates"],
    discovery_function=discover_sslcertificates,
    discovery_default_parameters={},
    discovery_ruleset_name="sslcertificates_inventory",
    discovery_ruleset_type=RuleSetType.MERGED,
    check_function=check_sslcertificates,
    check_default_parameters={
        'age': ("fixed", (90 * 86400.0, 60 * 86400.0)),
        'warnalgo': [ 'md5WithRSAEncryption', 'sha1WithRSAEncryption' ],
    },
    check_ruleset_name="sslcertificates",
)
