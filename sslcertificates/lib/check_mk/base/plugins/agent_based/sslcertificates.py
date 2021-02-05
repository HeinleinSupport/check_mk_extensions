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

def sslcertificates_name(line):
    return line[0]

def parse_sslcertificates(string_table):
    return string_table

register.agent_section(
    name="sslcertificates",
    parse_function=parse_sslcertificates,
)

# def discovery_sslcertificates(params, section_sslcertificates):
def discovery_sslcertificates(section):
    for line in section:
        service_labels=[]
        algosign = '/'
        if len(line) > 2:
            algosign = line[2]
        if algosign[0] == '/':
            # old agent plugin
            algosign = ''
        if algosign:
            service_labels.append(ServiceLabel('sslcertificates/algorithm', algosign))
        yield Service(item=sslcertificates_name(line), labels=service_labels)

def check_sslcertificates(item, params, section):
    warn, crit = params.get('age', (0, 0))
    warnalgos = params.get('warnalgo', [])
    ignore = params.get('ignore', None)

    for line in section:
        if item == sslcertificates_name(line):
            
            endtime = int(line[1])
            now = int(time.time())
            secondsremaining = endtime - now
            ignored = False

            algosign = '/'
            if len(line) > 2:
                algosign = line[2]
            if algosign[0] == '/':
                # old agent plugin
                algosign = ''
                subj = " ".join(line[2:])
            else:
                subj = " ".join(line[3:])
            yield Result(state=State.OK, summary="Subject: %s" % subj)

            if secondsremaining < 0:
                infotext = "expired %s ago on %s" % ( render.timespan(abs(secondsremaining)),
                                                      time.strftime("%c", time.gmtime(endtime)))
            else:
                infotext = "expires in %s on %s" % ( render.timespan(secondsremaining),
                                                     time.strftime("%c", time.gmtime(endtime)))
            if ignore and -secondsremaining > ignore[0]:
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

            if algosign:
                infotext = "Signature Algorithm: %s" % algosign
                if not ignored and algosign in warnalgos:
                    yield Result(state=State.WARN, summary=infotext)
                else:
                    yield Result(state=State.OK, summary=infotext)

register.check_plugin(
    name="sslcertificates",
    service_name="SSL Certificate in %s",
    sections=["sslcertificates"],
    discovery_function=discovery_sslcertificates,
    # discovery_default_parameters={},
    # discovery_ruleset_name="",
    # discovery_ruleset_type=register.RuleSetType.MERGED,
    check_function=check_sslcertificates,
    check_default_parameters={
        'age': ( 90, 60 ),
        'warnalgo': [ 'md5WithRSAEncryption', 'sha1WithRSAEncryption' ],
    },
    check_ruleset_name="sslcertificates",
)
