#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

register_check_parameters(
    subgroup_applications,
    "otrs",
    _("OTRS Queues"),
    Dictionary(
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
    ),
    TextAscii(title = _('OTRS Queue Name')),
    match_type = "dict",
)

