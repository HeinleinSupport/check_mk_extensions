#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2014 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>

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
    DictElement,
    Dictionary,
    Float,
    InputHint,
    LevelDirection,
    migrate_to_float_simple_levels,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    HostAndItemCondition,
    Topic,
)


#   .--Parameter-----------------------------------------------------------.
#   |          ____                                _                       |
#   |         |  _ \ __ _ _ __ __ _ _ __ ___   ___| |_ ___ _ __            |
#   |         | |_) / _` | '__/ _` | '_ ` _ \ / _ \ __/ _ \ '__|           |
#   |         |  __/ (_| | | | (_| | | | | | |  __/ ||  __/ |              |
#   |         |_|   \__,_|_|  \__,_|_| |_| |_|\___|\__\___|_|              |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

def _parameter_valuespec_ox_runtimestats():
    return Dictionary(
        elements = {
            'levels': DictElement(
                required=True,
                parameter_form=SimpleLevels(
                    title=Title("Battery capacity"),
                    help_text=Help("The meaning of these levels depend on the OX attribute the rule is applied to."),
                    migrate=migrate_to_float_simple_levels,
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Float(),
                    prefill_fixed_levels=InputHint((0.0, 0.0)),
                )),
        },
    )

rule_spec_ox_runtimestats = CheckParameters(
    name="open_xchange",
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_valuespec_ox_runtimestats,
    title=Title("Open-XChange Attributes"),
    help_text=Help("Thresholds for Open-XChange attributes"),
    condition=HostAndItemCondition(
        item_title=Title("Open-XChange Attribute")
    ),
)
