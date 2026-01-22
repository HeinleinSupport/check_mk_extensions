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

import shlex
from cmk.base.check_api import host_name
import cmk.base.config as config
from cmk.checkengine.fetcher import SourceType

def _creds_to_args(creds):
    args = ''
    if isinstance(creds, str):
        args += ' --v2c -C %s' % shlex.quote(creds)
    elif isinstance(creds, tuple):
        if creds[0] == 'noAuthNoPriv':
            args += ' -l %s' % shlex.quote(creds[1])
        if creds[0] == 'authNoPriv':
            args += ' -L "%s",' % creds[1]
            args += ' -l %s' % shlex.quote(creds[2])
            args += ' -x %s' % shlex.quote(creds[3])
        if creds[0] == 'authPriv':
            args += ' -L "%s","%s"' % (creds[1], creds[4])
            args += ' -l %s' % shlex.quote(creds[2])
            args += ' -x %s' % shlex.quote(creds[3])
            args += ' -X %s' % shlex.quote(creds[5])
    return args

def check_snmp_temperature_single_arguments(params):
    if 'hostname' in params:
        args = "-H %s" % shlex.quote(params['hostname'])
    else:
        args = "-H $HOSTADDRESS$"

    if 'creds' in params:
        args += _creds_to_args(params['creds'])
    else:
        config_cache = config.get_config_cache()
        ipaddress = config.lookup_ip_address(config_cache, host_name())
        snmp_config = config_cache.make_snmp_config(host_name(), ipaddress, SourceType.HOST)
        args += _creds_to_args(snmp_config.credentials)

    if "port" in params:
        args += " -P %d" % params["port"]
        
    if "timeout" in params:
        args += ' -t %d' % params["timeout"]

    args += ' -n temp -d %s -a temp -f' % shlex.quote(params["oid"])

    if "levels_upper" in params:
        args += ' -w %d -c %d' % params["levels_upper"]

    if "factor" in params:
        args += ' -i %dC' % params['factor']

    return args

def check_snmp_temperature_single_description(params):
    if 'description' in params:
        return 'Temperature %s' % params['description']
    
    return "Temperature %s" % params['oid']

active_check_info['snmp_temperature_single'] = {
    "command_line"        : "check_snmp_temperature.pl $ARG1$",
    "argument_function"   : check_snmp_temperature_single_arguments,
    "service_description" : check_snmp_temperature_single_description,
    "has_perfdata"        : True,
}


