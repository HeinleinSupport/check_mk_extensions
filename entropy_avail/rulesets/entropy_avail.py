#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2013 Heinlein Support GmbH
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
    DefaultValue,
    DictElement,
    Dictionary,
    Float,
    Integer,
    LevelDirection,
    migrate_to_float_simple_levels,
    migrate_to_integer_simple_levels,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    HostCondition,
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

def _parameter_valuespec_entropy_avail():
    return Dictionary(
        elements = {
            "percentage": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Minimum Entropy that has to be available in percent"),
                    migrate=migrate_to_float_simple_levels,
                    form_spec_template=Float(
                        unit_symbol="%",
                    ),
                    level_direction=LevelDirection.LOWER,
                    prefill_fixed_levels=DefaultValue((0.0, 0.0)),
                )),
            "absolute": DictElement(
                parameter_form=SimpleLevels(
                    title = Title("Minimum absolute Entropy that has to be available"),
                    migrate=migrate_to_integer_simple_levels,
                    form_spec_template=Integer(),
                    level_direction=LevelDirection.LOWER,
                    prefill_fixed_levels=DefaultValue((200, 100)),
                )),
        },
    )

rule_spec_entropy_avail = CheckParameters(
    name="entropy_avail",
    topic=Topic.OPERATING_SYSTEM,
    parameter_form=_parameter_valuespec_entropy_avail,
    title=Title("Entropy Available"),
    help_text=Help("Here you can override the default levels for the entropy Available check. You can either specify a absolut value or a percentage value."),
    condition=HostCondition(),
)