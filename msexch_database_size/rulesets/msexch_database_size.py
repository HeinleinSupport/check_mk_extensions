#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DataSize,
    DefaultValue,
    DictElement,
    Dictionary,
    Float,
    IECMagnitude,
    LevelDirection,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _migrate(params: object) -> dict:
    """Migrate legacy parameter formats."""
    if not isinstance(params, dict):
        # Very old format: just a size tuple
        return {"size": ("fixed", params) if params else ("no_levels", None)}
    migrated = dict(params)
    for key in ("size", "availSpace"):
        value = migrated.get(key)
        if value is None:
            migrated[key] = ("no_levels", None)
            continue
        if isinstance(value, tuple) and len(value) == 2 and not isinstance(value[0], str):
            # Legacy format: (warn, crit) -> ("fixed", (warn, crit))
            migrated[key] = ("fixed", value)
    return migrated


def _parameter_form():
    return Dictionary(
        title=Title("Thresholds for MS Exchange database size"),
        help_text=Help(
            "Deleting old mailboxes leads to white space that MS Exchange administrators"
            " might want to clean up."
        ),
        migrate=_migrate,
        elements={
            "size": DictElement(
                required=False,
                parameter_form=SimpleLevels(
                    title=Title("Impose limits on the size of the database"),
                    help_text=Help(
                        "The check will trigger a warning or critical state if the size"
                        " of the database exceeds these levels."
                    ),
                    form_spec_template=DataSize(
                        displayed_magnitudes=[
                            IECMagnitude.MEBI,
                            IECMagnitude.GIBI,
                            IECMagnitude.TEBI,
                        ],
                    ),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue(
                        value=(50 * 1024**3, 100 * 1024**3)
                    ),
                ),
            ),
            "availSpace": DictElement(
                required=False,
                parameter_form=SimpleLevels(
                    title=Title("Percentage of free Mailbox space"),
                    form_spec_template=Float(unit_symbol="%"),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue(value=(20.0, 40.0)),
                ),
            ),
        },
    )


rule_spec_msexch_database_size = CheckParameters(
    name="msexch_database_size",
    title=Title("MS Exchange Database Size"),
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_form,
    condition=HostAndItemCondition(
        item_title=Title("Name of the database"),
    ),
)
