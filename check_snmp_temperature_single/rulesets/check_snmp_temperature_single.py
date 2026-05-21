#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2013 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>
#

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

from cmk.rulesets.v1 import Help, Title, Message
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    FieldSize,
    InputHint,
    Integer,
    LevelDirection,
    LevelsType,
    migrate_to_integer_simple_levels,
    SimpleLevels,
    String,
)
from cmk.rulesets.v1.form_specs.validators import (
    LengthInRange,
    MatchRegex,
    NumberInRange,
)
from cmk.rulesets.v1.rule_specs import ActiveCheck, Topic
from cmk.gui.form_specs.unstable import LegacyValueSpec
from cmk.gui.watolib.attributes import SNMPCredentials

def _valuespec_active_checks_snmp_temperature_single():
    return Dictionary(
        elements = {
            "description": DictElement(
                required=True,
                parameter_form=String(
                    title=Title("Service Description"),
                    help_text=Help("Must be unique for every host. Defaults to command that is executed."),
                    field_size=FieldSize.MEDIUM,
                )),
            "hostname": DictElement(
                parameter_form=String(
                    title=Title("DNS Hostname or IP address"),
                    help_text=Help("You can specify a hostname or IP address different from IP address of the host as configured in your host properties."),
                    prefill=InputHint("$HOSTADDRESS$"),
                    custom_validate=[LengthInRange(min_value=1)],
                )),
            'port': DictElement(
                parameter_form=Integer(
                    title=Title("SNMP Port"),
                    help_text=Help("Default is 161."),
                    prefill=DefaultValue(161),
                    custom_validate=[NumberInRange(min_value=1, max_value=65535)],
                )),
            "timeout": DictElement(
                parameter_form=Integer(
                    title=Title("Seconds before connection times out"),
                    unit_symbol="sec",
                    prefill=InputHint(10),
                )),
            "creds": DictElement(
                parameter_form=LegacyValueSpec.wrap(SNMPCredentials(
                    help = "If not set, the SNMP credentials of the host will be used",
                ))),
            "oid": DictElement(
                required=True,
                parameter_form=String(
                    title=Title("OID to query"),
                    custom_validate=[MatchRegex(regex=r"(\.\d+)+", error_msg=Message("Please input a valid OID"))]
                )),
            "levels_upper": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Upper levels on Temperature"),
                    migrate=migrate_to_integer_simple_levels,
                    form_spec_template=Integer(
                        unit_symbol="°C",
                    ),
                    prefill_levels_type=DefaultValue(LevelsType.NONE),
                    prefill_fixed_levels=InputHint((0, 0)),
                    level_direction=LevelDirection.UPPER,
                )),
            "factor": DictElement(
                parameter_form=Integer(
                    title=Title("Factor"),
                    help_text=Help("What factor is used by the SNMP agent to express the temperature. A factor of 10 means to agent shows 330 when the temperature is 33 °C."),
                    prefill=InputHint(10),
                )),
        },
    )

rule_spec_check_snmp_temperature_single = ActiveCheck(
    title = Title("Check single Temperature via SNMP"),
    help_text = Help("Checks a single Temperature on one SNMP OID."),
    topic=Topic.ENVIRONMENTAL,
    name="snmp_temperature_single",
    parameter_form=_valuespec_active_checks_snmp_temperature_single,
)
