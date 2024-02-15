#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    Tuple,
    Integer,
    TextInput,
)

from cmk.gui.plugins.wato.utils import (
    rulespec_registry,
    CheckParameterRulespecWithItem,
    RulespecGroupCheckParametersEnvironment,
)

def _parameter_valuespec_wagner_racksens2_detector():
    return Dictionary(
        elements = [
            ( 'smoke_levels',
              Tuple(
                  title = _("Smoke Levels"),
                  elements = [
                      Integer(title = _("Warning at"), unit='%', default_value=3),
                      Integer(title = _("Critical at"), unit='%', default_value=5),
                  ]
            )),
            ( 'chamber_levels',
              Tuple(
                  title = _("Chamber Levels"),
                  elements = [
                      Integer(title = _("Warning at"), unit='%', default_value=10),
                      Integer(title = _("Critical at"), unit='%', default_value=20),
                  ]
            )),
        ],
        optional_keys = ['smoke_levels', 'chamber_levels'],
    )

rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="wagner_racksens2_detector",
        group=RulespecGroupCheckParametersEnvironment,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_wagner_racksens2_detector,
        title=lambda: _("Wagner Racksens2 Smoke Detector"),
        item_spec=lambda: TextInput(
            title=_("Sensor ID"), help=_("The identifier of the smoke detector.")
        ),
    ))
