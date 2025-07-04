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
    DictElement,
    Dictionary,
    Integer,
    InputHint,
    LevelDirection,
    migrate_to_integer_simple_levels,
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

def _parameter_valuespec_postfix_mailq_details():
    return Dictionary(
        elements = {
            'level': DictElement(
                required=True,
                parameter_form=SimpleLevels(
                    help_text=Help("These levels are applied to the number of Email that are currently in the specified mail queue."),
                    migrate=migrate_to_integer_simple_levels,
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Integer(
                        unit_symbol="mails",
                    ),
                    prefill_fixed_levels=InputHint((1000, 1500)),
                )),
        },
    )

rule_spec_postfix_mailq_details = CheckParameters(
    name="postfix_mailq_details",
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_valuespec_postfix_mailq_details,
    title=Title("Number of mails in specific mail queues"),
    condition=HostAndItemCondition(item_title=Title("Name of service")),
)
