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
    migrate_to_password,
    Password,
    String,
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

def _valuespec_aspsms() -> Dictionary:
    return Dictionary(
        elements = {
            "user_key": DictElement(
                parameter_form=String(
                    title = Title("User Key"),
                    help_text = Help("Configure the user key here. The key can be obtained from the "
                        "<a href=\"https://www.aspsms.com/apicredentials/\" target=\"_blank\">"
                        "aspsms.com</a> website."),
                    field_size = 40,
                )),
            "api_password": DictElement(
                parameter_form=Password(
                    title = Title("API Password"),
                    help_text = Help("You need to provide a valid API passowrd to be able to send notifications "
                        "using ASPSMS. Register and login to <a href=\"https://www.aspsms.com/apicredentials/\" "
                        "target=\"_blank\">ASPSMS</a> to obtain your API key."),
                    migrate=_migrate_password,
                )),
            "originator": DictElement(
                parameter_form=String(
                    title = Title("Originator"),
                    help_text = Help("You can set the originator of the message here."),
                    field_size = 40,
                )),
        }
    )

rule_spec_aspsms = NotificationParameters(
    name="aspsms",
    title=Title("SMS via aspsms.com"),
    topic=Topic.NOTIFICATIONS,
    parameter_form=_valuespec_aspsms,
)
