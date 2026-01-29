#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    DropdownChoice,
    Integer,
    TextInput,
    Tuple,
)

from cmk.gui.plugins.wato import (
    rulespec_registry,
    CheckParameterRulespecWithItem,
    RulespecGroupCheckParametersEnvironment,
)

def _parameter_valuespec_vertiv_geist_pdu_a2d_binary():
    return Dictionary(
        title = _("State Mapping"),
        help = _("Mapping of value to check state."),
        elements = [
            ( 'ok',
              DropdownChoice(
                  title = _("OK is"),
                  choices = [
                      ( 0, "0" ),
                      ( 1, "1" ),
                  ],
            )),
        ],
        required_keys = [ "ok" ],
    )

rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="vertiv_geist_pdu_a2d_binary",
        group=RulespecGroupCheckParametersEnvironment,
        match_type="first",
        parameter_valuespec=_parameter_valuespec_vertiv_geist_pdu_a2d_binary,
        title=lambda: _("Vertiv Geist PDU binary sensors"),
        item_spec=lambda: TextInput(
            title=_("Sensor Label"),
            help=_("The label of the sensor as configured in the device."),
        ),
    ))
