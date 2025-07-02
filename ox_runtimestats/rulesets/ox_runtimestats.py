#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
)

from cmk.gui.plugins.wato import (
    rulespec_registry,
    CheckParameterRulespecWithItem,
    Levels,
    RulespecGroupCheckParametersApplications,
)

def _item_spec_open_xchange():
    return TextAscii(
        title = _("Open-XChange Attribute"),
        allow_empty = False,
    )

def _parameter_valuespec_open_xchange():
    return Dictionary(
        help = _("Thresholds for Open-XChange attributes"),
        elements = [
            ("levels",
             Levels(
                 title = _('Levels'),
                 help = _('The meaning of these levels depend on the OX attribute the rule is applied to.'),
             )
            ),
        ],
        optional_keys = [],
    )

rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="open_xchange",
        group=RulespecGroupCheckParametersApplications,
        item_spec=_item_spec_open_xchange,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_open_xchange,
        title=lambda: _("Open-XChange Attributes"),
    ))
