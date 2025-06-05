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

from cmk.base.check_api import host_name
import cmk.base.config as config
from cmk.checkengine.fetcher import SourceType
from functools import reduce # type: ignore

from collections.abc import Iterator # type: ignore
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
        args += ['-v', '2c']
        args += ['-c', creds]
    elif isinstance(creds, tuple):
        args += ['-v', '3', '-l',  creds[0]]
        if creds[0] == 'noAuthNoPriv':
            args += ['-u', creds[1]]
        if creds[0] == 'authNoPriv':
            args += ['-a', creds[1]]
            args += ['-u', creds[2]]
            args += ['-A', creds[3]]
        if creds[0] == 'authPriv':
            args += ['-a', creds[1]]
            args += ['-u', creds[2]]
            args += ['-A', creds[3]]
            args += ['-x', creds[4]]
            args += ['-X', creds[5]]
    return args

def check_snmp_metric_arguments(params, host_config: HostConfig) -> Iterator[ActiveCheckCommand]:
    if 'creds' in params:
        args = _creds_to_args(params['creds'])
    else:
        config_cache = config.get_config_cache()
        ipaddress = config.lookup_ip_address(config_cache, host_name())
        snmp_config = config_cache.make_snmp_config(host_name(), ipaddress, SourceType.HOST)
        args = _creds_to_args(snmp_config.credentials)

    if "timeout" in params:
        args += ['-t', "%d" % params["timeout"]]

    if "factor" in params:
        args += ['--factor', "%f" % params["factor"]]

    if "offset" in params:
        args += ['--offset', "%f" % params["offset"]]

    if "unit" in params:
        args += ['--unit', params["unit"]]

    if "metric" in params:
        args += ['--metric', params["metric"]]

    if params.get("levels_upper", ("no_levels", None))[0] == "fixed":
        args += ['--warn', "%d" % params["levels_upper"][1][0]]
        args += ['--crit', "%d" % params["levels_upper"][1][1]]

    if params.get("levels_lower", ("no_levels", None))[0] == "fixed":
        args += ['--lwarn', "%d" % params["levels_lower"][1][0]]
        args += ['--lcrit', "%d" % params["levels_lower"][1][1]]

    if 'hostname' in params:
        hostname = params['hostname']
    else:
        hostname = "$HOSTADDRESS$"
    hostname = replace_macros(hostname, host_config.macros)

    if "port" in params:
        hostname += ":%d" % params["port"]
    
    args.append(hostname)

    args.append(params['oid'])
        
    yield ActiveCheckCommand(
        service_description=check_snmp_metric_description(params),
        command_arguments=args,
    )

def check_snmp_metric_description(params):
    return params['description']


active_check_snmp_metric = ActiveCheckConfig(
    name="snmp_metric",
    parameter_parser=noop_parser,
    commands_function=check_snmp_metric_arguments,
)