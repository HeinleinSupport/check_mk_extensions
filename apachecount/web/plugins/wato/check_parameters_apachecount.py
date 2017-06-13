#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

def apachecount_parameters(title, unit = "requests per second"):
    return Levels(
        title = title,
        unit = unit,
        default_difference = (2.0, 4.0),
        default_levels = (5.0, 10.0),
        )

register_check_parameters(
    subgroup_applications,
    "apachecount",
    _("Apache Requests Statistics"),
    Dictionary(
        elements = [
            ('sum', Checkbox(
                title = _('Status Code Summarization'),
                help = _('When checked the plugin will summarize the status codes in blocks of hundreds (100-199, 200-299, 300-399, 400-499, 500-599…). When checked levels have to be set on the hundreds (100, 200, 300, 400, 500…).'),
                label = _('Summarize Status Codes'),
            )),
            ('codes', ListOf(
                Tuple(
                    elements = [
                        Integer(
                            title = _('Status Code'),
                            help = _('Enter the HTTP status code for which the levels should be applied.'),
                            minvalue = 100,
                            maxvalue = 999,
                            default_value = 200,
                        ),
                        apachecount_parameters(_('Levels')),
                    ],
                ),
                title = _('Levels for Status Codes'),
            ))
        ],
        help = _('This ruleset defines the levels for the different Apache status codes collected from its logfile.'),
    ),
    False,
    match_type = "dict",
)

