#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2020 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>

#
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

# try:
#     from cmk.gui.i18n import _
#     from cmk.gui.plugins.wato import (
#         HostRulespec,
#         rulespec_registry,
#     )
#     from cmk.gui.cee.plugins.wato.agent_bakery.rulespecs.utils import RulespecGroupMonitoringAgentsAgentPlugins
#     from cmk.gui.valuespec import (
#         DropdownChoice,
#     )

#     def _valuespec_agent_config_wireguard():
#         return DropdownChoice(
#             title = _("WireGuard VPN (Linux)"),
#             help = _("This will deploy the agent plugin <tt>wireguard</tt> for monitoring the status of WireGuard VPNs."),
#             choices = [
#                 ( True, _("Deploy plugin for WireGuard VPNs") ),
#                 ( None, _("Do not deploy plugin for WireGuard VPNs") ),
#             ]
#         )

#     rulespec_registry.register(
#         HostRulespec(
#             group=RulespecGroupMonitoringAgentsAgentPlugins,
#             name="agent_config:wireguard",
#             valuespec=_valuespec_agent_config_wireguard,
#         ))

# except ModuleNotFoundError:
#     # RAW edition
#     pass

from cmk.rulesets.v1 import (
    Help,
    Label,
    Title,
)
from cmk.rulesets.v1.form_specs import (
    BooleanChoice,
    DefaultValue,
    DictElement,
    Dictionary,
)
from cmk.rulesets.v1.rule_specs import (
    AgentConfig,
    Topic,
)

#   .--Bakery--------------------------------------------------------------.
#   |                   ____        _                                      |
#   |                  | __ )  __ _| | _____ _ __ _   _                    |
#   |                  |  _ \ / _` | |/ / _ \ '__| | | |                   |
#   |                  | |_) | (_| |   <  __/ |  | |_| |                   |
#   |                  |____/ \__,_|_|\_\___|_|   \__, |                   |
#   |                                             |___/                    |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

def _migrate_from_bool_to_dict(param):
    if isinstance(param, bool):
        param = {"deploy": param}
    if isinstance(param, dict) and param == {}:
        param = {"deploy": True}
    return param

def _valuespec_agent_config_wireguard():
    return Dictionary(
        migrate=_migrate_from_bool_to_dict,
        elements = {
            "deploy": DictElement(
                required=True,
                parameter_form=BooleanChoice(
                    label=Label("Deploy plugin for WireGuard VPNs"),
                    prefill=DefaultValue(True),
                ),
            ),
        },
    )

rule_spec_wireguard_bakery = AgentConfig(
    name="wireguard",
    title=Title("WireGuard VPN (Linux)"),
    help_text=Help("This will deploy the agent plugin <tt>wireguard</tt> for WireGuard VPNs."),
    topic=Topic.APPLICATIONS,
    parameter_form=_valuespec_agent_config_wireguard,
)