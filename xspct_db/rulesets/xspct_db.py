#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2026 Heinlein Consulting GmbH
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
    Integer,
    InputHint,
    LevelDirection,
    migrate_to_integer_simple_levels,
    SingleChoice,
    SingleChoiceElement,
    SimpleLevels,
    validators,
)
from cmk.rulesets.v1.rule_specs import (
    AgentConfig,
    CheckParameters,
    DiscoveryParameters,
    HostAndItemCondition,
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

def _valuespec_agent_config_xspct_db():
    return Dictionary(
        elements={
            "deploy": DictElement(
                required=True,
                parameter_form=BooleanChoice(
                    label=Label("Deploy plugin for XSPCT DB"),
                    prefill=DefaultValue(True),
                )),
            "protocol": DictElement(
                parameter_form=SingleChoice(
                    title=Title("Protocol"),
                    help_text=Help("Protocol to access the /metrics endpoint"),
                    elements=[
                        SingleChoiceElement(name="http", title=Title("HTTP")),
                        SingleChoiceElement(name="https", title=Title("HTTPS")),
                    ],
                    prefill=DefaultValue("http"),
                )),
            "port": DictElement(
                parameter_form=Integer(
                    title=Title("Port"),
                    help_text=Help("Port number to access the /metrics endpoint"),
                    custom_validate=[validators.NumberInRange(min_value=1, max_value=65535)],
                    prefill=DefaultValue(11350),
                )),
        },
    )

rule_spec_xspct_db_bakery = AgentConfig(
    name="xspct_db",
    title=Title("XSPCT DB via Prometheus Exporter (Linux)"),
    help_text=Help("This will deploy the agent plugin <tt>xspct_db</tt> to check various XSPCT DB stats."),
    topic=Topic.APPLICATIONS,
    parameter_form=_valuespec_agent_config_xspct_db,
)
