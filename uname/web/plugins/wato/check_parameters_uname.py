#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

register_check_parameters(
    subgroup_os,
    "uname",
    _("Kernel Version Check"),
    Dictionary(
        elements = [
            ('release', RegExp( RegExp.prefix, title = _("Expected Release") ) ),
            ('version', RegExp( RegExp.prefix, title = _("Expected Version") ) ),
        ],
        help = _('The check <tt>uname</tt> monitors the kernel version.'),
    ),
    None,
    match_type = 'dict',
)

