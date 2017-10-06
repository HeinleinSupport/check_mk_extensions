#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

register_check_parameters(
    subgroup_applications,
    "postconf",
    _("Postfix Configuration Settings"),
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
    ),
    None,
    None
)

