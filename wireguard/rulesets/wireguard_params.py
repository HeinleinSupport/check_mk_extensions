#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (C) 2025 Heinlein Consulting GmbH
#          Robert Sander <r.sander@heinlein-support.de>
# Copyright (C) 2024 Matthias Henze - License: GNU General Public License v2
# Contact: mahescho@gmail.com

from cmk.rulesets.v1 import (
    Help,
    Label,
    Title,
)
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Integer,
    InputHint,
    LevelDirection,
    List,
    migrate_to_upper_float_levels,
    SimpleLevels,
    String,
    TimeMagnitude,
    TimeSpan,
    validators,
)
from cmk.rulesets.v1.rule_specs import (
    AgentConfig,
    CheckParameters,
    DiscoveryParameters,
    HostAndItemCondition,
    Topic,
)

def _parameter_valuespec_wireguard():
    return Dictionary (
        elements = {
            "timeout": DictElement(
                parameter_form=SimpleLevels(
                    title = Title('Timeout'),
                    # help_text = Help("Days until expiry of certificate"),
                    migrate = migrate_to_upper_float_levels,
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = TimeSpan(
                        displayed_magnitudes=[TimeMagnitude.DAY, TimeMagnitude.HOUR, TimeMagnitude.MINUTE, TimeMagnitude.SECOND],
                    ),
                    prefill_fixed_levels = InputHint(
                        value=(300.0, 3000.0),
                    ),
                )),
        }
    )

rule_spec_wireguard_data = CheckParameters(
    name="wireguard_data",
    topic=Topic.ENVIRONMENTAL,
    parameter_form=_parameter_valuespec_wireguard,
    title=Title("Wireguard"),
    condition=HostAndItemCondition(
        item_title=Title("Wireguard Peer"),
        item_form=String(
            help_text=Help("Peer"),
        )
    ),
)
