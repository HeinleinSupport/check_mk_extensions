#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    Integer,
    Tuple,
)

from cmk.gui.plugins.wato import (
    rulespec_registry,
    CheckParameterRulespecWithoutItem,
    RulespecGroupCheckParametersApplications,
)

def _parameter_valuespec_velocloud_pathnum():
    return Dictionary(
        title = _("Limits"),
        help = _("Size of all files and subdirectories"),
        elements = [
            ( 'levels_upper',
              Tuple(
                  title = _('Upper levels for the number of paths'),
                  elements = [
                      Integer(title = _("Warning at"), unit = 'paths', default_value=23),
                      Integer(title = _("Critical at"), unit = 'paths', default_value=25),
                  ],
              )),
        ],
        required_keys = [ "levels_upper" ],
    )

rulespec_registry.register(
    CheckParameterRulespecWithoutItem(
        check_group_name="velocloud_pathnum",
        group=RulespecGroupCheckParametersApplications,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_velocloud_pathnum,
        title=lambda: _("VeloCloud Path Limits"),
    ))
