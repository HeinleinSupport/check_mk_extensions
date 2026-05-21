#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2013 Heinlein Support GmbH
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

from cmk.base import config
from cmk.checkengine.fetcher import SourceType

from collections.abc import Iterator # type: ignore
from cmk.server_side_calls.v1 import (
    ActiveCheckCommand,
    ActiveCheckConfig,
    HostConfig,
    noop_parser,
    replace_macros,
)
from cmk.ccc.hostaddress import HostAddress, HostName

def _creds_to_args(creds):
    args = []
    if isinstance(creds, str):
        args += ['--v2c', '-C', creds]
    elif isinstance(creds, tuple):
        if creds[0] == 'noAuthNoPriv':
            args += ['-l', creds[1]]
        if creds[0] == 'authNoPriv':
            args += ['-L', creds[1]]
            args += ['-l', creds[2]]
            args += ['-x', creds[3]]
        if creds[0] == 'authPriv':
            args += ['-L', '"%s","%s"' % (creds[1], creds[4])]
            args += ['-l', creds[2]]
            args += ['-x', creds[3]]
            args += ['-X', creds[5]]
    return args

def check_snmp_temperature_single_arguments(params, host_config: HostConfig) -> Iterator[ActiveCheckCommand]:
    if 'creds' in params:
        args = _creds_to_args(params['creds'])
    else:
        loading_result = config.load(
            discovery_rulesets=(), get_builtin_host_labels=lambda x: {}
        )
        config_cache = loading_result.config_cache
        ip_lookup_config = config_cache.ip_lookup_config()
        host_name = HostName(host_config.name)
        ip_family = ip_lookup_config.default_address_family(host_name)
        ip_address = HostAddress(host_config.primary_ip_config.address)
        snmp_config = config_cache.make_snmp_config(host_name, ip_family, ip_address, SourceType.HOST, backend_override=None)
        args = _creds_to_args(snmp_config.credentials)

    if 'hostname' in params:
        hostname = params['hostname']
    else:
        hostname = "$HOSTADDRESS$"
    hostname = replace_macros(hostname, host_config.macros)

    args += ['-H', hostname]

    if "port" in params:
        args += ["-P", str(params["port"])]
        
    if "timeout" in params:
        args += ['-t', str(params["timeout"])]

    args += ['-n', 'temp', '-d', params["oid"], '-a', 'temp', '-f']

    if "levels_upper" in params:
        mode, levels = params["levels_upper"]
        if mode == "fixed":
            args += ['-w', str(levels[0]), '-c', str(levels[1])]

    if "factor" in params:
        args += ['-i', '%dC' % params['factor']]

    yield ActiveCheckCommand(
        service_description=check_snmp_temperature_single_description(params),
        command_arguments=args,
    )

def check_snmp_temperature_single_description(params):
    if 'description' in params:
        return 'Temperature %s' % params['description']
    
    return "Temperature %s" % params['oid']

active_check_snmp_temperature_single = ActiveCheckConfig(
    name="snmp_temperature_single",
    parameter_parser=noop_parser,
    commands_function=check_snmp_temperature_single_arguments,
)
