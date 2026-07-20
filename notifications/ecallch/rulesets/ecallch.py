#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2018 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>

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
    DictElement,
    Dictionary,
    FieldSize,
    migrate_to_password,
    Password,
    String,
    validators,
)
from cmk.rulesets.v1.rule_specs import (
    NotificationParameters,
    Topic,
)


def _migrate_password(model):
    if isinstance(model, str):
        model = ("password", model)
    model = migrate_to_password(model)
    return model

def _valuespec_ecallch() -> Dictionary:
    return Dictionary(
        title=Title("Configure the ecall.ch connection"),
        elements = {
            "username": DictElement(
                parameter_form=String(
                    title=Title("User Name"),
                    help_text=Help("Configure the user name here."),
                    field_size=FieldSize.MEDIUM,
                    custom_validate=[validators.LengthInRange(min_value=1)],
            )),
            "password": DictElement(
                parameter_form=Password(
                    title=Title("Password"),
                    help_text=Help("You need to provide a valid passowrd to be able to send notifications."),
                    custom_validate=[validators.LengthInRange(min_value=1)],
                    migrate=_migrate_password,
            )),
        }
    )

rule_spec_notification_ecallch = NotificationParameters(
    name="ecallch",
    title=Title("ecall.ch"),
    parameter_form=_valuespec_ecallch,
    topic=Topic.NOTIFICATIONS,
)
