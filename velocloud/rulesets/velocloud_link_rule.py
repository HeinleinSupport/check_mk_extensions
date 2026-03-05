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
    LevelDirection,
    migrate_to_float_simple_levels,
    SimpleLevels,
    TimeMagnitude,
    TimeSpan,
)
from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    HostAndItemCondition,
    Topic,
)


def _parameter_valuespec_velocloud_link():
    return Dictionary(
        title=Title("Levels for Link parameters"),
        ignored_elements=["raw_state"],
        elements={
            "rx_latency": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Upper RX Latency Levels"),
                    migrate=migrate_to_float_simple_levels,
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=TimeSpan(
                        displayed_magnitudes=[TimeMagnitude.MILLISECOND, TimeMagnitude.SECOND],
                    ),
                    prefill_fixed_levels=InputHint(value=(0.02, 0.05)),
                )),
            "tx_latency": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Upper TX Latency Levels"),
                    migrate=migrate_to_float_simple_levels,
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=TimeSpan(
                        displayed_magnitudes=[TimeMagnitude.MILLISECOND, TimeMagnitude.SECOND],
                    ),
                    prefill_fixed_levels=InputHint(value=(0.02, 0.05)),
                )),
        },
    )

rule_spec_velocloud_link = CheckParameters(
    name="velocloud_link",
    topic=Topic.NETWORKING,
    parameter_form=_parameter_valuespec_velocloud_link,
    title=Title("VeloCloud Link thresholds"),
    condition=HostAndItemCondition(item_title=Title("Link Interface")),
)
