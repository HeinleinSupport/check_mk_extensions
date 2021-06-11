#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    Tuple,
    ListOfStrings,
    TextAscii,
)

from cmk.gui.plugins.wato import (
    rulespec_registry,
    CheckParameterRulespecWithItem,
    Levels,
    RulespecGroupCheckParametersApplications,
)

def _item_spec_otrs():
    return TextAscii(title = _('OTRS Queue Name'))

def _parameter_valuespec_otrs():
    return Dictionary(
        title = _('Number of Tickets in Queue'),
        help = _('Count the number of tickets in a queue based on their state.'),
        elements = [
            ('levels', ListOf(
                Tuple(
                    elements = [
                        ListOfStrings(
                            title = _('OTRS Ticket State'),
                            help = _('The ticket state as reported in the check output.'),
                        ),
                        Levels(
                            title = _('Number of Tickets in this state'),
                            unit = _('tickets'),
                            default_difference = (20, 40),
                            default_levels = (50, 100),
                        ),
                    ],
                    title = 'OTRS Queue Size',
                ),
                title = 'List of States',
            )),
        ],
        optional_keys = None,
    )

rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="otrs",
        group=RulespecGroupCheckParametersApplications,
        item_spec=_item_spec_otrs,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_otrs,
        title=lambda: _("OTRS Queues"),
    ))
