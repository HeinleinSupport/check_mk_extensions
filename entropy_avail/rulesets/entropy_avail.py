#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    Percentage,
    Tuple,
    Integer,
)

from cmk.gui.plugins.wato import (
    rulespec_registry,
    CheckParameterRulespecWithoutItem,
    RulespecGroupCheckParametersOperatingSystem,
)

def _parameter_valuespec_entropy_avail():
    return Dictionary(
        help = _("Here you can override the default levels for the entropy Available check."
                   "You can either specify a absolut value or a percentage value."),
        elements = [
            ( "percentage",
                Tuple(
                title = _("Minimum Entropy that has to be available in percent"),
                elements = [
                    Percentage(title = _("Warning at"), default_value = 0.0, unit = _("% left")),
                    Percentage(title = _("Critical at"), default_value = 0.0, unit = _("% left")),
                ]
                )
            ),
            ( "absolute",
                Tuple(
                title = _("Minimum absolute Entropy that has to be available"),
                elements = [
                    Integer(title = _("Warning if below than"), default_value = 200),
                    Integer(title = _("Critical if below than"), default_value = 100),
                ],
                ),
            ),
        ],
    )

rulespec_registry.register(
    CheckParameterRulespecWithoutItem(
        check_group_name="entropy_avail",
        group=RulespecGroupCheckParametersOperatingSystem,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_entropy_avail,
        title=lambda: _("Entropy Available"),
    ))
