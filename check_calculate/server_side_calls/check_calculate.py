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


from collections.abc import Iterator # type: ignore
from cmk.server_side_calls.v1 import (
    ActiveCheckCommand,
    ActiveCheckConfig,
    HostConfig,
    noop_parser,
)

def check_calculate_arguments(params, host_config: HostConfig) -> Iterator[ActiveCheckCommand]:

    args = ['-d', params.get('description')]
    args += ['-l', params.get('label')]
    args += ['-m', params.get('metric')]
    args += ['-o', params.get('levels_lower').__repr__()]
    args += ['-u', params.get('levels_upper').__repr__()]
    args += ['-e', params.get('expression').replace('\n', '')]

    yield ActiveCheckCommand(
        service_description=check_calculate_description(params),
        command_arguments=args,
    )

def check_calculate_description(params):
    return '%s' % params.get('description')

active_check_check_calculate = ActiveCheckConfig(
    name="calculate",
    parameter_parser=noop_parser,
    commands_function=check_calculate_arguments,
)
