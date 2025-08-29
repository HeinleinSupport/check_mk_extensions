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

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Float,
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
    Message,
    MatchRegex,
    NumberInRange,
)
from cmk.rulesets.v1.rule_specs import ActiveCheck, Topic

def _valuespec_active_checks_snmp_metric():
    return Dictionary(
        ignored_elements = ["creds"],
        elements = {
            "description": DictElement(
                required=True,
                parameter_form = String(
                    title = Title("Service Description"),
                    help_text = Help("Must be unique for every host."),
                    field_size = 30,
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
            # ( "creds",
            #   SNMPCredentials(
            #       help = _("If not set, the SNMP credentials of the host will be used"),
            #   )),
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
            "levels_lower": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Lower levels"),
                    migrate = migrate_to_integer_simple_levels,
                    level_direction = LevelDirection.LOWER,
                    form_spec_template = Integer(),
                    prefill_levels_type = DefaultValue(LevelsType.NONE),
                    prefill_fixed_levels = InputHint((0, 0)),
                )),
            "factor": DictElement(
                parameter_form = Float(
                    title = Title("Value factor"),
                    help_text = Help("A Factor of 10 means that the value reported is ten times the real value, e.g. the OID contains 245, but the real temperature is 24.5°C"),
                    prefill = DefaultValue(1.0),
                )),
            "offset": DictElement(
                parameter_form = Float(
                    title = Title("Value offset"),
                    help_text = Help("An offset that gets added (with a positive value) to the value or subtracted (with a negative value) from the value after applying the value factor."),
                    prefill = DefaultValue(0.0),
                )),
            "metric": DictElement(
                parameter_form = String(
                    title = Title("Metric name"),
                    help_text = Help("Name of the metric for performance data. If obmitted, no performance data will be generated."),
                )),
            "unit": DictElement(
                parameter_form = String(
                    title = Title("Unit"),
                    help_text = Help("Unit of the value. Used for display."),
                )),
        },
    )


rule_spec_check_snmp_metric = ActiveCheck(
    title = Title("Check SNMP Metric"),
    help_text = Help("Checks SNMP Metrics with the Nagios plugin <tt>check_snmp_metric</tt>."),
    topic=Topic.GENERAL,
    name="snmp_metric",
    parameter_form=_valuespec_active_checks_snmp_metric,
)
