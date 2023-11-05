#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2020 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# tails. You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

from cmk.gui.valuespec import TextInput, Checkbox
from cmk.gui.cee.plugins.wato.alert_handling import register_alert_handler_parameters

register_alert_handler_parameters("auto_ack", Dictionary(
    optional_keys = ['username', 'host_problems', 'service_problems'],
    elements = [
        ("comment", TextInput(
            title = _("Comment"),
            help = _("You need to provide a comment for the acknowledgment."),
            allow_empty = False,
        )),
        ("username", TextInput(
            title = _("Automation Account"),
            help = _("Automation account for the ack via REST-API. If not set, the account 'automation' will be used."),
            allow_empty = False,
        )),
        ("host_problems", Checkbox(
            title = _("Host Problems"),
            label = _("Only Host Problems"),
            help = _("Only auto-ack host problems, not service problems"),
        )),
        ("service_problems", Checkbox(
            title = _("Service Problems"),
            label = _("Only Service Problems"),
            help = _("Only auto-ack service problems"),
        )),
    ]
))

