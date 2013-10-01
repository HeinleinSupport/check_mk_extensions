#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2013 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  This file is distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

group = "checkparams"

subgroup_applications = _("Applications, Processes &amp; Services")

register_check_parameters(
    subgroup_applications,
    "postfix_mailq_details",
    _("Number of mails in specific mail queues"),
    Tuple(
          help = _("These levels are applied to the number of Email that are "
                   "currently in the specified mail queue."),
          elements = [
              Integer(title = _("Warning at"), unit = _("mails"), default_value = 1000),
              Integer(title = _("Critical at"), unit = _("mails"), default_value = 1500),
          ]
    ),
    TextAscii(
        title = _("Name of service"),
        allow_empty = False,
    ),
    None
)

