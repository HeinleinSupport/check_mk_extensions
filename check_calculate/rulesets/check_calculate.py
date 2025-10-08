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

from cmk.rulesets.v1 import (
    Help,
    Label,
    Title,
)
from cmk.rulesets.v1.form_specs import (
    BooleanChoice,
    DefaultValue,
    DictElement,
    Dictionary,
    Float,
    Integer,
    InputHint,
    LevelDirection,
    migrate_to_float_simple_levels,
    MultilineText,
    SingleChoice,
    SingleChoiceElement,
    SimpleLevels,
    String,
)
from cmk.rulesets.v1.rule_specs import (
    ActiveCheck,
    AgentConfig,
    CheckParameters,
    DiscoveryParameters,
    HostAndItemCondition,
    Topic,
)


def _vs_levels(title, level_direction):
    return SimpleLevels(
        title=Title(title),
        migrate=migrate_to_float_simple_levels,
        form_spec_template=Float(),
        level_direction=level_direction,
        prefill_fixed_levels=InputHint((0.0, 0.0)),
    )

def _valuespec_active_checks_calculate():
    return Dictionary(
        elements = {
            'description': DictElement(
                required=True,
                parameter_form=String(
                    title=Title('Service description'),
                )),
            'label': DictElement(
                required=True,
                parameter_form=String(
                    title=Title('Label for check output'),
                )),
            'metric': DictElement(
                required=True,
                parameter_form=String(
                    title=Title('Metric name for calculated value'),
                )),
            'levels_upper': DictElement(
                parameter_form=_vs_levels(
                    title='Upper levels',
                    level_direction=LevelDirection.UPPER,
                )),
            'levels_lower': DictElement(
                parameter_form=_vs_levels(
                    title='Lower levels',
                    level_direction=LevelDirection.LOWER,
                )),
            'expression': DictElement(
                required=True,
                parameter_form=MultilineText(
                    title=Title('Expression'),
                    help_text=Help('The expression used here is compatible with the expression from custom graphs.'),
                )),
        },
    )

rule_spec_check_calculate = ActiveCheck(
    title = Title("Calculate on Perfdata"),
    topic=Topic.GENERAL,
    name="calculate",
    parameter_form=_valuespec_active_checks_calculate,
)
