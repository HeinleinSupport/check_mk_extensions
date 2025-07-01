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
    migrate_to_password,
    Password,
    String,
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

def _migrate_password(model):
    if isinstance(model, str):
        model = ("password", model)
    model = migrate_to_password(model)
    return model

def _valuespec_agent_config_ox_filestore():
    return Dictionary(
        migrate=_migrate_from_alternative_to_dict,
        elements = {
            "deploy": DictElement(
                required=True,
                parameter_form=BooleanChoice(
                    label=Label("Deploy the SSL certificates plugin"),
                    prefill=DefaultValue(True),
                )),
            "username": DictElement(
                required=True,
                parameter_form=String(
                    title=Title("Username for OX admin master"),
                )),
            "password": DictElement(
                required=True,
                parameter_form=Password(
                    title=Title("Password for OX admin master"),
                    migrate=_migrate_password,
                )),
        }
    )

rule_spec_agent_config_ox_filestore = AgentConfig(
    name="ox_filestore",
    title=Title("Open-Xchange Filestore Check (Linux)"),
    help_text=Help("This will deploy the agent plugin <tt>ox_filestore</tt> for checking Open-Xchange file stores."),
    topic=Topic.APPLICATIONS,
    parameter_form=_valuespec_agent_config_ox_filestore,
)
