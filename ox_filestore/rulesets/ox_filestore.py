#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    Integer,
    Tuple,
)

from cmk.gui.plugins.wato import (
    rulespec_registry,
    CheckParameterRulespecWithItem,
    RulespecGroupCheckParametersApplications,
)

def _item_spec_ox_filestore():
    return TextAscii(
        title = _("Filestore URL"),
        help = _('OX filestore URL starting with "file:/". You can make the rule apply only to certain filestores of the specified hosts. Do this by specifying explicit items to match here. <b>Hint:</b> make sure to enter the filestore URL only, not the full Service description. <b>Note:</b> the match is done on the <u>beginning</u> of the item in question. Regular expressions are interpreted, so appending a $ will force an exact match.')
    )

def _parameter_valuespec_ox_filestore():
    return Dictionary(
        title = _('Levels for Open-Xchange file stores'),
        elements = [
            ( 'reserved', Tuple(
                title = _('Reserved'),
                elements = [
                    Integer(title = _("Warning at"), unit = _("%"), default_value = 80),
                    Integer(title = _("Critical at"), unit = _("%"), default_value = 90),
                ])),
            ( 'used', Tuple(
                title = _('Used'),
                elements = [
                    Integer(title = _("Warning at"), unit = _("%"), default_value = 80),
                    Integer(title = _("Critical at"), unit = _("%"), default_value = 90),
                ])),
            ( 'ent', Tuple(
                title = _('Entities'),
                elements = [
                    Integer(title = _("Warning at"), unit = _("%"), default_value = 80),
                    Integer(title = _("Critical at"), unit = _("%"), default_value = 90),
                ])),
          ]
    )

rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="ox_filestore",
        group=RulespecGroupCheckParametersApplications,
        item_spec=_item_spec_ox_filestore,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_ox_filestore,
        title=lambda: _("Open-Xchange Filestores Levels"),
    ))
