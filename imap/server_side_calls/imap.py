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

from collections.abc import Iterator, Mapping, Sequence # type: ignore
from enum import StrEnum # type: ignore

from pydantic import BaseModel

from cmk.server_side_calls.v1 import (
    ActiveCheckCommand,
    ActiveCheckConfig,
    HostConfig,
    Secret,
    noop_parser,
    replace_macros,
)


class LevelsType(StrEnum):
    NO_LEVELS = "no_levels"
    FIXED = "fixed"

def convert_options(options) -> Iterator[str | Secret]:

    state_string = {
        0: 'ok',
        1: 'warn',
        2: 'crit',
        3: 'unknown',
    }

    if 'ssl' in options:
        yield "-S"
        yield "-p"
        if 'port' in options:
            yield str(options['port'])
        else:
            yield "993"
    else:
        if 'port' in options and options['port'] != 143:
            yield "-p"
            yield str(options['port'])

    if "ip_version" in options:
        if options['ip_version'] == 'ipv4':
            yield '-4'
        else:
            yield '-6'

    if 'send' in options:
        yield '-s'
        yield options['send']

    if 'expect' in options:
        yield '-e'
        yield options['expect']

    if 'quit' in options:
        yield '-q'
        yield options['quit']

    if 'refuse' in options:
        yield '-r'
        yield state_string.get(options['refuse'])

    if 'mismatch' in options:
        yield '-M'
        yield state_string.get(options['mismatch'])

    if 'jail' in options:
        yield '-j'

    if 'maxbytes' in options:
        yield '-m'
        yield str(options['maxbytes'])

    if 'delay' in options:
        yield '-d'
        yield str(options['delay'])

    if 'certificate_age' in options:
        match options["certificate_age"]:
            case (LevelsType.FIXED, (float(warn), float(crit))):
                yield '-D'
                days_warn = int(warn / 86400)
                days_crit = int(crit / 86400)
                yield f'{days_warn},{days_crit}'

    if "response_time" in options:
        match options["response_time"]:
            case (LevelsType.FIXED, (float(warn), float(crit))):
                yield "-w"
                yield str(warn)
                yield "-c"
                yield str(crit)

    if 'timeout' in options:
        yield '-t'
        yield str(options['timeout'])


def generate_imap_commands(
    params: Mapping[str, object],
    host_config: HostConfig,
) -> Iterator[ActiveCheckCommand]:
    macros = host_config.macros
    options = params["settings"]
    if params["service_desc"].startswith('^'):
        service_desc = params["service_desc"][1:]
    else:
        service_desc = "IMAP %s" % params["service_desc"]
    if "hostname" not in params or not params['hostname']:
        if options.get('ip_version') == 'ipv6' and '$HOST_ADDRESS_6$' in macros:
            params["hostname"] = "$HOST_ADDRESS_6$"
        else:
            params["hostname"] = "$HOSTADDRESS$"
    args = ['-H', replace_macros(params["hostname"], macros)]
    args.extend(list(convert_options(options)))
    yield ActiveCheckCommand(
        service_description=service_desc,
        command_arguments=args,
    )

active_check_imap = ActiveCheckConfig(
    name="imap",
    parameter_parser=noop_parser,
    commands_function=generate_imap_commands,
)
