#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2016 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>
#

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

group = "agents/" + _("Agent Plugins")

register_rule(group,
    "agent_config:dir_size",
    Alternative(
        title = _("Directory Size"),
        help = _("This will deploy the agent plugin <tt>dir_size</tt> "
                 "for checking directory sizes. <b>Note:</b> If you want "
                 "to configure several directories to look into"
                 ", then simply create several rules. In this ruleset "
                 "<b>all</b> matching rules "
                 "are being executed, not only the first one. "),
        style = "dropdown",
        elements = [
            Dictionary(
                title = _("Deploy the directory size plugin"),
                elements = [
                   ( "directories",
                     ListOfStrings(
                        title = _("Directories to compute size for"),
                        valuespec = TextAscii(
                            size = 80,
                            regex = "^/[^ \t]+/$",
                            regex_error = _("Directory paths must begin and end with <tt>/</tt> and must not contain spaces."),
                       ),
                       allow_empty = False,

                     )
                   ),
                ],
                optional_keys = False,
            ),
            FixedValue(None, title = _("Do not deploy the directory size plugin"), totext = _("(disabled)") ),
        ]
    ),
    match = "all",
)

