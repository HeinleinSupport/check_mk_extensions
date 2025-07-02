#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    ListOf,
    TextAscii,
    Transform,
    Tuple,
)

from cmk.gui.plugins.wato import (
    rulespec_registry,
    CheckParameterRulespecWithoutItem,
    RulespecGroupCheckParametersApplications,
)

def _parameter_valuespec_postconf():
    return Transform(
        Dictionary(
            elements = [
                ( 'config',
                  ListOf(
                      Tuple(
                          show_titles = True,
                          orientation = "horizontal",
                          elements = [
                              TextAscii( title = _("Name of Configuration Variable"), ),
                              TextAscii( title = _("Expected Value"), ),
                          ]
                      ),
                      add_label = _("Add Variable"),
                      help = _('The check <tt>postconf</tt> monitors the Postfix configuration. Every configuration variable can be checked against a specific value.'),
                )),
            ],
            optional_keys = [],
        ),
        forth = lambda v: isinstance(v, list) and {
            'config': v
        } or v,
    )

rulespec_registry.register(
    CheckParameterRulespecWithoutItem(
        check_group_name="postconf",
        group=RulespecGroupCheckParametersApplications,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_postconf,
        title=lambda: _("Postfix Configuration Settings"),
    ))
