#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2016 Heinlein Support GmbH
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
    Title,
)
from cmk.rulesets.v1.form_specs import (
    DataSize,
    DictElement,
    Dictionary,
    IECMagnitude,
    InputHint,
    LevelDirection,
    migrate_to_upper_integer_levels,
    SimpleLevels,
    String,
)
from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    HostAndItemCondition,
    Topic,
)

def _parameter_valuespec_dir_size():
    return Dictionary(
        title = Title("Limits"),
        help_text = Help("Size of all files and subdirectories"),
        elements = {
            "levels_upper": DictElement(
                required=True,
                parameter_form=SimpleLevels(
                    title=Title("Upper levels for the total size"),
                    migrate=migrate_to_upper_integer_levels,
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=InputHint((10, 20)),
                    form_spec_template=DataSize(
                        displayed_magnitudes=[
                            IECMagnitude.BYTE,
                            IECMagnitude.KIBI,
                            IECMagnitude.MEBI,
                            IECMagnitude.GIBI,
                            IECMagnitude.TEBI,
                            IECMagnitude.PEBI,
                        ]
                    ),
                ),
            ),
        },
    )

rule_spec_dir_size = CheckParameters(
    name="dir_size",
    topic=Topic.STORAGE,
    parameter_form=_parameter_valuespec_dir_size,
    title=Title("Directory Size Limits"),
    condition=HostAndItemCondition(
        item_title=Title("Directory"),
        item_form=String(
            help_text=Help("The path of the directory"),
        )
    ),
)
