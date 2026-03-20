#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    SingleChoice,
    SingleChoiceElement,
)
from cmk.rulesets.v1.rule_specs import AgentConfig, Topic


def _migrate(params: object) -> dict:
    """Migrate legacy DropdownChoice values (True/None) to new Dictionary format."""
    if isinstance(params, dict):
        return params
    if params:
        return {"deploy": "deploy"}
    return {"deploy": "do_not_deploy"}


def _parameter_form():
    return Dictionary(
        migrate=_migrate,
        elements={
            "deploy": DictElement(
                required=True,
                parameter_form=SingleChoice(
                    title=Title("MS Exchange Database Size (Windows)"),
                    help_text=Help(
                        "This will deploy the agent plugin msexch_database_size.ps1"
                        " for monitoring the size of MS Exchange databases."
                    ),
                    elements=[
                        SingleChoiceElement(
                            name="deploy",
                            title=Title("Deploy plugin for MS Exchange database size"),
                        ),
                        SingleChoiceElement(
                            name="do_not_deploy",
                            title=Title(
                                "Do not deploy plugin for MS Exchange database size"
                            ),
                        ),
                    ],
                    prefill=DefaultValue("deploy"),
                ),
            ),
        },
    )


rule_spec_msexch_database_size_bakery = AgentConfig(
    name="msexch_database_size",
    title=Title("MS Exchange Database Size (Windows)"),
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_form,
)
