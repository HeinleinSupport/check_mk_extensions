#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.rulesets.v1 import (
    Help,
    Label,
    Title,
)
from cmk.rulesets.v1.form_specs import (
    BooleanChoice,
    CascadingSingleChoice,
    CascadingSingleChoiceElement,
    DefaultValue,
    DictElement,
    Dictionary,
    FixedValue,
    Integer,
    List,
    String,
    validators,
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

def _migrate_to_dict(param):
    if isinstance(param, str):
        param = {
            "deploy": (param == "autodetect"),
            "instances": ('autodetect', True),
        }
    if isinstance(param, tuple):
        instances = []
        for ip, port in param[1]:
            instance = {
                "ip": ip,
            }
            if port:
                instance["port"] = port
            instances.append(instance)
        param = {
            "deploy": True,
            "instances": (
                "manual",
                instances,
            )
        }
    if isinstance(param, dict) and param == {}:
        param = {"deploy": True}
    return param

def _valuespec_agent_config_memcached():
    return Dictionary(
        migrate=_migrate_to_dict,
        elements = {
            "deploy": DictElement(
                required=True,
                parameter_form=BooleanChoice(
                    label=Label("Deploy plugin for memcached"),
                    prefill=DefaultValue(True),
                ),
            ),
            "instances": DictElement(
                required=True,
                parameter_form=CascadingSingleChoice(
                    title=Title("Instances"),
                    elements=[
                        CascadingSingleChoiceElement(
                            name="autodetect",
                            title=Title("Autodetect Instances"),
                            parameter_form=FixedValue(
                                value=True,
                            ),
                        ),
                        CascadingSingleChoiceElement(
                            name="manual",
                            title=Title("Manually configure instances"),
                            parameter_form=List(
                                element_template=Dictionary(
                                    elements={
                                        "ip": DictElement(
                                            required=True,
                                            parameter_form=String(
                                                title=Title("IP address"),
                                            ),
                                        ),
                                        "port": DictElement(
                                            parameter_form=Integer(
                                                title=Title("TCP Port"),
                                                custom_validate=[validators.NumberInRange(min_value=1, max_value=65535)],
                                            ),
                                        ),
                                    }
                                ),
                                add_element_label=Label("Add new instance"),
                                remove_element_label=Label("Remove this instance"),
                            )
                        ),
                    ]
                )
            ),
        },
    )

rule_spec_memcached_bakery = AgentConfig(
    name="memcached",
    title=Title("Memcached instances (Linux)"),
    help_text=Help("If you activate this option, then the agent plugin <tt>memcached</tt> will be deployed. For each configured or detected memcached instance there will be one new service with detailed statistics of the current number of clients and processes and their various states."),
    topic=Topic.APPLICATIONS,
    parameter_form=_valuespec_agent_config_memcached,
)