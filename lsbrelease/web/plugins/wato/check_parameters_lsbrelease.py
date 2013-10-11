#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

subgroup_os =           _("Operating System Resources")

register_check_parameters(
    subgroup_os,
    "lsbrelease",
    _("Distribution Version Check"),
    ListOf(
        Tuple(
            show_titles = True,
            orientation = "horizontal",
            elements = [
                TextAscii( title = _("Name of Distribution"), ),
                TextAscii( title = _("Expected Version"), ),
                ]
            ),
        add_label = _("Add Distribution"),
        help = _('The check <tt>lsbrelease</tt> monitors the distribution version. The start of the lsb_release <tt>Description</tt> field has to match against the "Name of Distribution", then the versions will be compared.'),
    ),
    None,
    None
)

