#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2021 Heinlein Consulting GmbH
#          Robetr Sander <r.sander@heinlein-support.de>
#
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
    Title,
)
from cmk.rulesets.v1.form_specs import (
    DictElement,
    Dictionary,
    InputHint,
    Integer,
    LevelDirection,
    migrate_to_integer_simple_levels,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    HostCondition,
    Topic,
)

def _parameter_valuespec_velocloud_pathnum():
    return Dictionary(
        title=Title("Limits"),
        elements={
            "levels_upper": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Upper levels for the number of paths"),
                    migrate=migrate_to_integer_simple_levels,
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Integer(unit_symbol="paths"),
                    prefill_fixed_levels=InputHint(value=(23, 25)),
                )),
            "levels_lower": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Lower levels for the number of paths"),
                    migrate=migrate_to_integer_simple_levels,
                    level_direction=LevelDirection.LOWER,
                    form_spec_template=Integer(unit_symbol="paths"),
                    prefill_fixed_levels=InputHint(value=(5, 1)),
                )),
        }
    )

rule_spec_velocloud_pathnum = CheckParameters(
    name="velocloud_pathnum",
    topic=Topic.NETWORKING,
    parameter_form=_parameter_valuespec_velocloud_pathnum,
    title=Title("VeloCloud Path Limits"),
    condition=HostCondition(),
)
