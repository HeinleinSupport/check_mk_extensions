#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

register_check_parameters(
    subgroup_applications,
    "netifaces_rbl",
    _("RBL"),
    ListOfStrings(
        title = _("List of RBLs to check against"),
        add_label = _("Add RBL"),
        help = _('The check <tt>netifaces.rbl</tt> monitors IP addresses of the host against the RBLs defined here.'),
    ),
    TextAscii(
        title = _("Interface Address"),
        help = _("The IP address as returned by the netifaces agent plugin."),
        allow_empty = False
    ),
    None
)

