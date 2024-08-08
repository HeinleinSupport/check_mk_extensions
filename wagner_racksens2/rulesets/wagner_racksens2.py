#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DictElement,
    Dictionary,
    Integer,
    InputHint,
    LevelDirection,
    migrate_to_integer_simple_levels,
    SimpleLevels,
    String,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic

def _parameter_form_wagner_racksens2_detector() -> Dictionary:
    return Dictionary(
        elements = {
           "smoke_levels": DictElement(
              parameter_form=SimpleLevels(
                  title = Title("Smoke Levels"),
                  level_direction = LevelDirection.UPPER,
                  form_spec_template = Integer(unit_symbol="%"),
                  migrate=migrate_to_integer_simple_levels,
                  prefill_fixed_levels=InputHint(value=(3, 5)),
              )),
            "chamber_levels": DictElement(
              parameter_form=SimpleLevels(
                  title = Title("Chamber Levels"),
                  level_direction = LevelDirection.UPPER,
                  form_spec_template = Integer(unit_symbol="%"),
                  migrate=migrate_to_integer_simple_levels,
                  prefill_fixed_levels=InputHint(value=(10, 20)),
              )),
        },
    )

rule_spec_wagner_racksens2_detector = CheckParameters(
    name="wagner_racksens2_detector",
    topic=Topic.ENVIRONMENTAL,
    parameter_form=_parameter_form_wagner_racksens2_detector,
    title=Title("Wagner Racksens2 Smoke Detector"),
    condition=HostAndItemCondition(
        item_title=Title("Sensor ID"),
        item_form=String(help_text=Help("The identifier of the smoke detector.")),
    ),
)
