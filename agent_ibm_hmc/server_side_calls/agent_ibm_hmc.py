#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2024 Heinlein Consulting GmbH
#          Robert Sander <r.sander@heinlein-support.de>

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

from cmk.base.plugins.bakery.bakery_api.v1 import quote_shell_string

from collections.abc import Iterable # pyright: ignore[reportShadowedImports]

from cmk.server_side_calls.v1 import HostConfig, noop_parser, SpecialAgentCommand, SpecialAgentConfig


def _special_agent_ibm_hmc_arguments(params, host_config: HostConfig) -> Iterable[SpecialAgentCommand]:
    args = []

    try:
        args += ["-H", host_config.primary_ip_config.address]
    except ValueError:
        args += ["-H", host_config.name]

    args += ["-U", quote_shell_string(params['username'])]

    if 'ssh_id' in params:
        args += ["-I", quote_shell_string(params['ssh_id'])]

    yield SpecialAgentCommand(command_arguments=args)

special_agent_ibm_hmc = SpecialAgentConfig(
    name="ibm_hmc",
    commands_function=_special_agent_ibm_hmc_arguments,
    parameter_parser=noop_parser,
)
