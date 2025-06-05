#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    Tuple,
    Integer,
)

from cmk.gui.plugins.wato import (
    rulespec_registry,
    CheckParameterRulespecWithoutItem,
    RulespecGroupCheckParametersApplications,
)

def _parameter_valuespec_amavis():
    return Dictionary(
        elements = [
            ( 'busy_childs',
              Tuple(
                  title = _("Busy child processes"),
                  elements = [
                      Integer(title = _("Warning at"), unit='%', default_value=75),
                      Integer(title = _("Critical at"), unit='%', default_value=95),
                  ]
            )),
        ],
        optional_keys = [],
    )

rulespec_registry.register(
    CheckParameterRulespecWithoutItem(
        check_group_name="amavis",
        group=RulespecGroupCheckParametersApplications,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_amavis,
        title=lambda: _("Amavis Statistics"),
    ))
