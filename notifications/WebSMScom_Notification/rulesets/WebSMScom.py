#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-


from cmk.rulesets.v1 import (
    Title,
)
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Password,
    SingleChoice,
    SingleChoiceElement,
)
from cmk.rulesets.v1.rule_specs import (
    NotificationParameters,
    Topic,
)

def _value_spec_WebSMScom():
    return Dictionary(
        title=Title("Send notifications via websms.com"),
        elements={
            "token": DictElement(
                parameter_form=Password(
                    title=Title("Access Token"),
                )),
            "art": DictElement(
                parameter_form=SingleChoice(
                    title=Title("SMS oder Sprachnachricht"),
                    elements=[
                        SingleChoiceElement(
                            name="default",
                            title=Title("SMS"),
                        ),
                        SingleChoiceElement(
                            name="voice",
                            title=Title("Sprachnachricht"),
                        ),
                        SingleChoiceElement(
                            name="complete",
                            title=Title("SMS und Sprachnachricht"),
                        ),
                    ],
                    prefill=DefaultValue("default"),
                )),
        }
    )

rule_spec_WebSMScom = NotificationParameters(
    name="WebSMScom",
    title=Title("WebSMScom"),
    topic=Topic.NOTIFICATIONS,
    parameter_form=_value_spec_WebSMScom,
)
