#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2026 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2. This file is  distributed
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

def _valuespec_agent_config_ipmisel():
    return Dictionary(
        elements={
            "deploy": DictElement(
                required=True,
                parameter_form=BooleanChoice(
                    label=Label("Deploy plugin for IPMI System Event Log"),
                    prefill=DefaultValue(True),
                ),
            )
        },
    )

rule_spec_ipmisel_bakery = AgentConfig(
    name="ipmisel",
    title=Title("IPMI System Event Log (Linux)"),
    help_text=Help("This will deploy the agent plugin <tt>ipmisel</tt> to fetch the IPMI System Events. The agent section generated is logwatch compatible."),
    topic=Topic.SERVER_HARDWARE,
    parameter_form=_valuespec_agent_config_ipmisel,
)
