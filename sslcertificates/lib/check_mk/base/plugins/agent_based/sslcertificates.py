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

from .agent_based_api.v1 import register, render, Result, Metric, State, check_levels, ServiceLabel, Service
import time
import json

def parse_sslcertificates(string_table):
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

register.agent_section(
    name="sslcertificates",
    parse_function=parse_sslcertificates,
)

def discover_sslcertificates(params, section):
    for name, data in section.items():
        if 'min_lifetime' in params and 'starts' in data:
            if data['expires'] - data['starts'] < params['min_lifetime']:
                continue
        sl = []
        if data.get('issuer_hash'):
            sl.append(ServiceLabel(u'sslcertificates/issuer_hash', data['issuer_hash']))
        if data.get('issuer'):
            sl.append(ServiceLabel(u'sslcertificates/issuer', data['issuer']))
        if data.get('algosign'):
            sl.append(ServiceLabel(u'sslcertificates/algorithm', data['algosign']))
        yield Service(item=name, labels=sl)

def check_sslcertificates(item, params, section):
    warn, crit = params.get('age', (0, 0))
    warnalgos = params.get('warnalgo', [])
    ignore = params.get('ignore', None)

    if item in section:
        data = section[item]
        
        now = int(time.time())
        secondsremaining = data['expires'] - now
        ignored = False

        yield Result(state=State.OK, summary="Subject: %s" % data['subj'])

        if secondsremaining < 0:
            infotext = "expired %s ago on %s" % ( render.timespan(abs(secondsremaining)),
                                                  time.strftime("%c", time.gmtime(data['expires'])))
        else:
            infotext = "expires in %s on %s" % ( render.timespan(secondsremaining),
                                                 time.strftime("%c", time.gmtime(data['expires'])))
        if ignore and -secondsremaining > ignore[0] * 86400:
            yield Result(state=State.OK, summary=infotext + ', ignored because "%s"' % ignore[1])
            ignored = True
        else:
            if secondsremaining > 0:
                yield from check_levels(secondsremaining,
                    levels_lower=(warn * 86400, crit * 86400),
                    metric_name='lifetime_remaining',
                    label='Lifetime Remaining',
                    render_func=render.timespan,
                    )
            else:
                yield from check_levels(secondsremaining,
                    levels_lower=(warn * 86400, crit * 86400),
                    metric_name='lifetime_remaining',
                    label='Expired',
                    render_func=lambda x: "%s ago" % render.timespan(abs(x)),
                    )

        if data.get('algosign'):
            infotext = "Signature Algorithm: %s" % data['algosign']
            if not ignored and data['algosign'] in warnalgos:
                yield Result(state=State.WARN, summary=infotext)
            else:
                yield Result(state=State.OK, summary=infotext)

register.check_plugin(
    name="sslcertificates",
    service_name="SSL Certificate in %s",
    sections=["sslcertificates"],
    discovery_function=discover_sslcertificates,
    discovery_default_parameters={},
    discovery_ruleset_name="sslcertificates_inventory",
    discovery_ruleset_type=register.RuleSetType.MERGED,
    check_function=check_sslcertificates,
    check_default_parameters={
        'age': ( 90, 60 ),
        'warnalgo': [ 'md5WithRSAEncryption', 'sha1WithRSAEncryption' ],
    },
    check_ruleset_name="sslcertificates",
)
