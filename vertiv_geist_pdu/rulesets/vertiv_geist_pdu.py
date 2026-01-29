#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2023 Heinlein Support GmbH
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

from cmk.rulesets.v1 import Title, Help
from cmk.rulesets.v1.form_specs import DefaultValue, DictElement, Dictionary, Integer
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic
from cmk.rulesets.v1.form_specs.validators import NumberInRange

def _parameter_form():
        return Dictionary(
        title = Title("State Mapping"),
        help_text = Help("Mapping of value to check state."),
        elements = {
            "ok": DictElement(
                required=True,
                parameter_form=Integer(
                    title=Title("OK is"),
                    prefill=DefaultValue(0),
                    custom_validate=[NumberInRange(min_value=0, max_value=1)],
                )
            ),
            },
    )

rule_spec_vertiv_geist_pdu_a2d_binary = CheckParameters(
    name = "vertiv_geist_pdu_a2d_binary",
    title = Title("Vertiv Geist PDU binary sensors"),
    topic = Topic.ENVIRONMENTAL,
    parameter_form = _parameter_form,
    condition = HostAndItemCondition(item_title=Title("Sensor Label")),
)
