#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2021 Heinlein Support GmbH
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
    TimeMagnitude,
    TimeSpan,
)
from cmk.rulesets.v1.rule_specs import (
    AgentConfig,
    Topic,
)

def _migrate_from_alternative_to_dict(param):
    if isinstance(param, dict) and param == {}:
        param = {"deploy": True}
    if isinstance(param, bool):
        param = {"deploy": param}
    if not param:
        param = {"deploy": False}
    if "deploy" not in param:
        param["deploy"] = True
    return param

def _valuespec_agent_config_proxmox_provisioned():
    return Dictionary(
        migrate=_migrate_from_alternative_to_dict,
        elements = {
            "deploy": DictElement(
                required=True,
                parameter_form=BooleanChoice(
                    label=Label("Deploy plugin for Proxmox Storage"),
                    prefill=DefaultValue(True),
                ),
            ),
            "interval": DictElement(
                parameter_form = TimeSpan(
                    title = Title("Run asynchronously"),
                    label = Label("Interval for collecting data"),
                    migrate = float,
                    prefill = DefaultValue(300.0),
                    displayed_magnitudes = [TimeMagnitude.HOUR, TimeMagnitude.MINUTE],
            )),
        },
    )

rule_spec_proxmox_provisioned_bakery = AgentConfig(
    name="proxmox_provisioned",
    title=Title("Proxmox Provisioned Storage (Linux)"),
    help_text=Help("This will deploy the agent plugin <tt>proxmox_provisioned</tt> for monitoring storage space."),
    topic=Topic.OPERATING_SYSTEM,
    parameter_form=_valuespec_agent_config_proxmox_provisioned,
)