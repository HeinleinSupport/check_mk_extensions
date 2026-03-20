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
    CascadingSingleChoice,
    CascadingSingleChoiceElement,
    DictElement,
    Dictionary,
    FixedValue,
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

# Map display names to state keys used in agent_based
_LINK_STATES = [
    ("1", "Initial"),
    ("2", "Dead"),
    ("3", "Unusable"),
    ("4", "Quiet"),
    ("5", "Standby"),
    ("6", "Unstable"),
    ("7", "Stable"),
    ("8", "Unknown"),
]

_STATE_CHOICES = [
    CascadingSingleChoiceElement(
        name="ok",
        title=Title("OK"),
        parameter_form=FixedValue(value="ok"),
    ),
    CascadingSingleChoiceElement(
        name="warn",
        title=Title("WARN"),
        parameter_form=FixedValue(value="warn"),
    ),
    CascadingSingleChoiceElement(
        name="crit",
        title=Title("CRIT"),
        parameter_form=FixedValue(value="crit"),
    ),
    CascadingSingleChoiceElement(
        name="unknown",
        title=Title("UNKNOWN"),
        parameter_form=FixedValue(value="unknown"),
    ),
]


def _state_mapping_elements() -> dict:
    """Build DictElements for each VPN link state."""
    elements = {}
    for state_id, state_name in _LINK_STATES:
        elements[f"vpn_state_{state_id}"] = DictElement(
            parameter_form=CascadingSingleChoice(
                title=Title(f"State: {state_name}"),
                elements=_STATE_CHOICES,
            ),
            required=False,
        )
    return elements


def _parameter_valuespec_velocloud_link():
    state_elements = _state_mapping_elements()
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
            **state_elements,
        },
    )

rule_spec_velocloud_link = CheckParameters(
    name="velocloud_link",
    topic=Topic.NETWORKING,
    parameter_form=_parameter_valuespec_velocloud_link,
    title=Title("VeloCloud Link thresholds"),
    condition=HostAndItemCondition(item_title=Title("Link Interface")),
)
