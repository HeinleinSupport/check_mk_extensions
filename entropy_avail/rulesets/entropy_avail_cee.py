#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2020 Heinlein Support GmbH
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
    if not param:
        param = {"deploy": False}
    return param

def _valuespec_agent_config_entropy_avail():
    return Dictionary(
        elements={
            "deploy": DictElement(
                required=True,
                parameter_form=BooleanChoice(
                    label=Label("Deploy plugin for Entropy Check"),
                    prefill=DefaultValue(True),
                ),
            )
        },
        migrate=_migrate_from_bool_to_dict,
    )

rule_spec_entropy_avail_bakery = AgentConfig(
    name="entropy_avail",
    title=Title("Entropy Available (Linux)"),
    help_text=Help("This will deploy the agent plugin <tt>entropy_avail</tt> for monitoring the available entropy."),
    topic=Topic.OPERATING_SYSTEM,
    parameter_form=_valuespec_agent_config_entropy_avail,
)
