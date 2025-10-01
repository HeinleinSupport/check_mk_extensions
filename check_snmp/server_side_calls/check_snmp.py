#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2021 Heinlein Support GmbH
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

import cmk.base.config as config
from cmk.checkengine.fetcher import SourceType
from functools import reduce # pyright: ignore[reportShadowedImports]
import shlex # pyright: ignore[reportShadowedImports]

from collections.abc import Iterator # pyright: ignore[reportShadowedImports]
from cmk.server_side_calls.v1 import (
    ActiveCheckCommand,
    ActiveCheckConfig,
    HostConfig,
    noop_parser,
    replace_macros,
)

def _creds_to_args(creds):
    args = []
    if isinstance(creds, str):
        args += ['-P', '2c']
        args += ['-C', creds]
    elif isinstance(creds, tuple):
        args += ['-P', '3', '-L',  creds[0]]
        if creds[0] == 'noAuthNoPriv':
            args += ['-U', creds[1]]
        if creds[0] == 'authNoPriv':
            args += ['-a', creds[1]]
            args += ['-U', creds[2]]
            args += ['-A', creds[3]]
        if creds[0] == 'authPriv':
            args += ['-a', creds[1]]
            args += ['-U', creds[2]]
            args += ['-A', creds[3]]
            args += ['-x', creds[4]]
            args += ['-X', creds[5]]
    return args

def _all_none(l):
    return not (reduce(lambda x,y: x or y, l))

def _list_to_args(para, l):
    if _all_none(l):
        return []
    return [para, ",".join(map(lambda x: str(x) if x else '', l))]

def check_snmp_arguments(params, host_config: HostConfig) -> Iterator[ActiveCheckCommand]:
    if 'hostname' in params:
        hostname = params['hostname']
    else:
        hostname = "$HOSTADDRESS$"
    hostname = replace_macros(hostname, host_config.macros)

    args = ["-H", hostname]

    if 'creds' in params:
        args += _creds_to_args(params['creds'])
    else:
        config_cache = config.get_config_cache()
        snmp_config = config_cache.make_snmp_config(host_config.name, host_config.primary_ip_config.address, SourceType.HOST, backend_override=None)
        args += _creds_to_args(snmp_config.credentials)

    if "port" in params:
        args += ["-p", params["port"]]

    if "timeout" in params:
        args += ['-t', "%d" % params["timeout"]]

    oids = []
    warn = []
    crit = []
    for query in params['query']:
        oids.append(query['oid'])
        levels_upper = query.get('levels_upper')
        if isinstance(levels_upper, tuple) and levels_upper[0] == "fixed":
            warn.append(levels_upper[1][0])
            crit.append(levels_upper[1][1])
        else:
            warn.append(None)
            crit.append(None)
    if oids:
        args += ["-m", "ALL", "-o", ",".join(map(shlex.quote, oids))]
    args += _list_to_args('-w', warn)
    args += _list_to_args('-c', crit)

    if 'match' in params:
        mode, value = params['match']
        if mode == 'string':
            args += ["-s", shlex.quote(value)]
        if mode == 'ereg':
            args += ["-r", shlex.quote(value)]
        if mode == 'eregi':
            args += ["-R", shlex.quote(value)]

    if 'invert' in params:
        args += ['--invert-search']

    if 'rate' in params:
        args += ['--rate', '--rate-multiplier', params['rate']]

    if "offset" in params:
        args += ['--offset', "%f" % params["offset"]]
        
    yield ActiveCheckCommand(
        service_description=check_snmp_description(params),
        command_arguments=args,
    )

def check_snmp_description(params):
    return params['description']

active_check_snmp = ActiveCheckConfig(
    name="snmp",
    parameter_parser=noop_parser,
    commands_function=check_snmp_arguments,
)
