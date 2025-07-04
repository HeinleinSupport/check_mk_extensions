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
    InputHint,
    String,
    TimeMagnitude,
    TimeSpan,
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

def _migrate_from_alternative_to_dict(param):
    if isinstance(param, dict) and param == {}:
        param = {"deploy": True}
    if isinstance(param, bool):
        param = {"deploy": param}
    if not param:
        param = {"deploy": False}
    if "deploy" not in param:
        param["deploy"] = True
    if "1" in param:
        param["one"] = param["1"]
        del(param["1"])
    if "2" in param:
        param["two"] = param["2"]
        del(param["2"])
    return param

def _valuespec_agent_config_postfix_mailq_details():
    return Dictionary(
        elements={
            "deploy": DictElement(
                required=True,
                parameter_form=BooleanChoice(
                    label=Label("Deploy the Postfix queue details plugin"),
                    prefill=DefaultValue(True),
                )),
            "one": DictElement(
                parameter_form=Dictionary(
                    title=Title("First group"),
                    elements={
                        "QUEUES": DictElement(
                            required=True,
                            parameter_form=String(
                                title=Title("Queues"),
                                prefill=InputHint("active incoming"),
                            )),
                        "AGE": DictElement(
                            required=True,
                            parameter_form=TimeSpan(
                                title=Title("Count emails older than"),
                                prefill=InputHint(300.0),
                                migrate=float,
                                displayed_magnitudes=[ TimeMagnitude.HOUR, TimeMagnitude.MINUTE ],
                            )),
                    }
                )),
            "two": DictElement(
                parameter_form=Dictionary(
                    title=Title("Second group"),
                    elements={
                        "QUEUES": DictElement(
                            required=True,
                            parameter_form=String(
                                title=Title("Queues"),
                                prefill=InputHint("deferred"),
                            )),
                        "AGE": DictElement(
                            required=True,
                            parameter_form=TimeSpan(
                                title=Title("Count emails younger than"),
                                prefill=InputHint(300.0),
                                migrate=float,
                                displayed_magnitudes=[ TimeMagnitude.HOUR, TimeMagnitude.MINUTE ],
                            )),
                    }
                )),
        },
        migrate=_migrate_from_alternative_to_dict,
    )

rule_spec_postfix_mailq_details_bakery = AgentConfig(
    name="postfix_mailq_details",
    title=Title("Postfix Queue Details (Linux)"),
    help_text=Help("This ruleset will deploy the agent plugin <tt>postfix_mailq_details</tt>."),
    topic=Topic.APPLICATIONS,
    parameter_form=_valuespec_agent_config_postfix_mailq_details,
)
