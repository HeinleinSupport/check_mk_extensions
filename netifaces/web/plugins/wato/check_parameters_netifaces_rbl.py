#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

register_check_parameters(
    subgroup_applications,
    "netifaces_rbl",
    _("RBL"),
    Dictionary(
        title = _("List of RBLs to check against"),
        help = _('The check <tt>netifaces.rbl</tt> monitors IP addresses of the host against the RBLs defined here.'),
        elements = [
            ( 'warn',
                ListOfStrings(
                    title = _("WARN"),
                    help = _('This list contains the RBLs that generate a WARNING state.'),
                ),
            ),
            ( 'crit',
                ListOfStrings(
                    title = _('CRIT'),
                    help = _('This list contains the RBLs that generate a CRITICAL state.'),
                    default_value = ['ix.dnsbl.manitu.net', 'bl.spamcop.net', 'zen.spamhaus.org'],
                ),
            ),
        ],
    ),
    TextAscii(
        title = _("Interface Address"),
        help = _("The IP address as returned by the netifaces agent plugin."),
        allow_empty = False
    ),
    match_type = 'dict',
)

