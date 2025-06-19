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
    List,
    String,
    validators,
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

def _valuespec_agent_config_mailman_queues():
    return Dictionary(
        migrate=_migrate_from_alternative_to_dict,
        elements = {
            "deploy": DictElement(
                required=True,
                parameter_form=BooleanChoice(
                    label=Label("Deploy the MailMan queues plugin"),
                    prefill=DefaultValue(True),
                ),
            ),
            "queues": DictElement(
                parameter_form = List(
                    title = Title("Queues to look into for mail files"),
                    help_text = Help("One queue name per line.<br />The default queues are <tt>bounces</tt>, <tt>in</tt>, <tt>out</tt> and <tt>shunt</tt>."),
                    element_template = String(
                        field_size=80,
                        custom_validate=[
                            validators.MatchRegex(
                                regex = r"^[^ \t*/]+$",
                                error_msg = "Queues must not contain spaces, / and *.",
                            ),
                        ],
                    ),
                    editable_order=False,
            )),
        },
    )

rule_spec_mailman_queues_bakery = AgentConfig(
    name="mailman_queues",
    title=Title("Mailman queues (Linux)"),
    help_text=Help("This will deploy the agent plugin <tt>mailman_queues</tt> for checking Mailman queues.<br />The default queues are <tt>bounces</tt>, <tt>in</tt>, <tt>out</tt> and <tt>shunt</tt>."),
    topic=Topic.APPLICATIONS,
    parameter_form=_valuespec_agent_config_mailman_queues,
)
