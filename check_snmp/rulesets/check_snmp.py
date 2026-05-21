#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2021 Heinlein Support GmbH
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

from cmk.rulesets.v1 import Help, Label, Title, Message
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    FieldSize,
    FixedValue,
    Float,
    InputHint,
    Integer,
    LevelDirection,
    LevelsType,
    List,
    MatchingScope,
    migrate_to_integer_simple_levels,
    RegularExpression,
    SimpleLevels,
    CascadingSingleChoice,
    CascadingSingleChoiceElement,
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

def _valuespec_active_checks_snmp():
    return Dictionary(
        elements = {
            "description": DictElement(
                required=True,
                parameter_form = String(
                    title = Title("Service Description"),
                    help_text = Help("Must be unique for every host."),
                    field_size = FieldSize.MEDIUM,
                    custom_validate = [LengthInRange(min_value=1)],
                )),
            "hostname": DictElement(
                parameter_form = String(
                    title = Title("DNS Hostname or IP address"),
                    help_text = Help("You can specify a hostname or IP address different from IP address of the host as configured in your host properties."),
                    prefill = DefaultValue("$HOSTADDRESS$"),
                    custom_validate = [LengthInRange(min_value=1)],
                )),
            "port": DictElement(
                parameter_form = Integer(
                    title = Title("SNMP Port"),
                    help_text = Help("Default is 161."),
                    custom_validate=[NumberInRange(min_value=1, max_value=65535)],
                    prefill=DefaultValue(161),
                )),
            "timeout": DictElement(
                parameter_form = Integer(
                    title = Title("Seconds before connection times out"),
                    unit_symbol = "s",
                    prefill = DefaultValue(10),
                )),
            "creds": DictElement(
                parameter_form=LegacyValueSpec.wrap(
                    SNMPCredentials(
                        help = "If not set, the SNMP credentials of the host will be used",
                    )),
                ),
            "query": DictElement(
                parameter_form=List(
                    title=Title("OIDs to query"),
                    add_element_label=Label("Add OID"),
                    element_template=Dictionary(
                        elements={
                            "oid": DictElement(
                                required = True,
                                parameter_form = String(
                                    title = Title("OID to query"),
                                    custom_validate = [
                                        MatchRegex(
                                            regex = r"^(\.\d+)+$",
                                            error_msg = Message("Value entered is not an OID."),
                                        ),
                                    ],
                                )),
                            "levels_upper": DictElement(
                                parameter_form = SimpleLevels(
                                    title = Title("Upper levels"),
                                    migrate = migrate_to_integer_simple_levels,
                                    level_direction = LevelDirection.UPPER,
                                    form_spec_template = Integer(),
                                    prefill_levels_type = DefaultValue(LevelsType.NONE),
                                    prefill_fixed_levels = InputHint((0, 0)),
                                )),
                        }
                    )
                )),
            "match": DictElement(
                parameter_form=CascadingSingleChoice(
                    title=Title("Matching on the OID value"),
                    elements=[
                        CascadingSingleChoiceElement(
                            name="string",
                            title=Title("String"),
                            parameter_form=String(
                                label=Label("string to match exactly")
                            )),
                        CascadingSingleChoiceElement(
                            name="ereg",
                            title=Title("Regex"),
                            parameter_form=RegularExpression(
                                help_text=Help("Return OK state (for that OID) if extended regular expression matches"),
                                label=Label("regular expression"),
                                predefined_help_text=MatchingScope.INFIX,
                            )),
                        CascadingSingleChoiceElement(
                            name="eregi",
                            title=Title("Regexi"),
                            parameter_form=RegularExpression(
                                help_text=Help("Return OK state (for that OID) if case-insensitive extended regular expression matches"),
                                label=Label("case insensitive regular expression"),
                                predefined_help_text=MatchingScope.INFIX,
                            )),
                    ]
                )),
            "invert": DictElement(
                parameter_form=FixedValue(
                    title=Title("Invert Match"),
                    help_text=Help("Invert search result (CRITICAL if found)"),
                    value="Invert search result",
                )),
            "rate": DictElement(
                parameter_form=Integer(
                    title=Title("Rate Calculation"),
                    help_text=Help("Enable rate calculation. Converts rate per second. For example, set mulitplier to 60 to convert to per minute."),
                    prefill=DefaultValue(1),
                    label=Label("Rate Multiplier"),
                    unit_symbol="s",
                )),
            "offset": DictElement(
                parameter_form = Float(
                    title = Title("Value offset"),
                    help_text = Help("An offset that gets added (with a positive value) to the value or subtracted (with a negative value) from the value after applying the value factor."),
                    prefill = DefaultValue(0.0),
                )),
        },
    )


rule_spec_check_snmp = ActiveCheck(
    title = Title("Check SNMP OID"),
    help_text = Help("Checks SNMP OIDs with the Nagios plugin <tt>check_snmp</tt>."),
    topic=Topic.GENERAL,
    name="snmp",
    parameter_form=_valuespec_active_checks_snmp,
)
