#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    CascadingDropdown,
    Dictionary,
    FixedValue,
    Float,
    ListOf,
    ListOfStrings,
    MonitoringState,
    TextAscii,
    Transform,
    Tuple,
)

from cmk.gui.plugins.wato import (
    rulespec_registry,
    CheckParameterRulespecWithoutItem,
    HostRulespec,
    RulespecGroupCheckParametersOperatingSystem,
)

def transform_lsbrelease_parameter_rules(p):
    if isinstance(p, list):
        return { 'distributions': p }
    return p

def _parameter_valuespec_lsbrelease():
    return Transform(
        Dictionary(
            elements=[
                ("distributions",
                 ListOf(
                     Tuple(
                         show_titles = True,
                         orientation = "horizontal",
                         elements = [
                             TextAscii( title = _("Name of Distribution"), ),
                             TextAscii( title = _("Expected Version"), ),
                         ]
                     ),
                     title=_("List of Distributions"),
                     add_label = _("Add Distribution"),
                     help = _('The check <tt>lsbrelease</tt> monitors the distribution version. The start of the lsb_release <tt>Description</tt> field has to match against the "Name of Distribution", then the versions will be compared.'),
                 )),
            ],
            required_keys=['distributions'],
        ),
        forth=transform_lsbrelease_parameter_rules,
    )

rulespec_registry.register(
    CheckParameterRulespecWithoutItem(
        check_group_name="lsbrelease",
        group=RulespecGroupCheckParametersOperatingSystem,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_lsbrelease,
        title=lambda: _("Distribution Version Check"),
    ))
