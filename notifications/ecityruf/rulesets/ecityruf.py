#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# tails. You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

from cmk.rulesets.v1 import (
    Help,
    Title,
)
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    FieldSize,
    Integer,
    InputHint,
    migrate_to_password,
    MultilineText,
    Password,
    String,
    validators,
)
from cmk.rulesets.v1.rule_specs import (
    NotificationParameters,
    Topic,
)

def _migrate_config(model):
    if "from" in model:
        model["from_address"] = model["from"]
        del(model["from"])
    return model

def _valuespec_ecityruf() -> Dictionary:
    return Dictionary(
        migrate=_migrate_config,
        title=Title("Configure the e*Cityruf connection"),
        elements={
            "from_address": DictElement(
                parameter_form=String(
                    title=Title("From: Address"),
                    custom_validate=[validators.EmailAddress()],
                    field_size=FieldSize.LARGE,
                )),
            "host_subject": DictElement(
                parameter_form=String(
                    title=Title("Subject for host notifications"),
                    help_text=Help("Here you are allowed to use all macros that are defined in the notification context."),
                    macro_support=True,
                    prefill=DefaultValue("Check_MK: $HOSTNAME$ - $EVENT_TXT$"),
                    field_size=FieldSize.LARGE,
                )),
            "service_subject": DictElement(
                parameter_form=String(
                    title=Title("Subject for service notifications"),
                    help_text=Help("Here you are allowed to use all macros that are defined in the notification context."),
                    macro_support=True,
                    prefill=DefaultValue("Check_MK: $HOSTNAME$/$SERVICEDESC$ $EVENT_TXT$"),
                    field_size=FieldSize.LARGE,
                )),
            "common_body": DictElement(
                parameter_form=MultilineText(
                    title=Title("Body head for both host and service notifications"),
                    monospaced=True,
                    macro_support=True,
                    prefill=DefaultValue("""Host:     $HOSTNAME$
Alias:    $HOSTALIAS$
Address:  $HOSTADDRESS$
"""),
                )),
            "host_body": DictElement(
                parameter_form=MultilineText(
                    title=Title("Body tail for host notifications"),
                    monospaced=True,
                    macro_support=True,
                    prefill=DefaultValue("""Event:    $EVENT_TXT$
Output:   $HOSTOUTPUT$
Perfdata: $HOSTPERFDATA$
$LONGHOSTOUTPUT$
"""),
                )),
            "service_body": DictElement(
                parameter_form=MultilineText(
                    title=Title("Body tail for service notifications"),
                    monospaced=True,
                    macro_support=True,
                    prefill=DefaultValue("""Service:  $SERVICEDESC$
Event:    $EVENT_TXT$
Output:   $SERVICEOUTPUT$
Perfdata: $SERVICEPERFDATA$
$LONGSERVICEOUTPUT$
"""),
                )),
        }
    )

rule_spec_notification_ecityruf = NotificationParameters(
    name="ecityruf",
    title=Title("e*Cityruf"),
    parameter_form=_valuespec_ecityruf,
    topic=Topic.NOTIFICATIONS,
)
