#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

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

group = "activechecks"

register_rule(group,
    "active_checks:git",
    Tuple(
        title = _("Check GIT service"),
        help = _("Checks GIT. "),
        elements = [
            Dictionary(
                title = _("Optional parameters"),
                elements = [
                    ( "repourl",
                      TextAscii(
                            title = _("Repo URL"),
                            default_value = "https://github.com/HeinleinSupport/check_mk.git",
                            allow_empty = False,
                            help = _("You can specify a GIT repo URL."))),
                    ( "reponame",
                      TextAscii(
                            title = _("Repo NAME"),
                            default_value = "check_mk addons",
                            allow_empty = False,
                            help = _("You can specify a name for the GIT repo."))),
                    ]
                )
            ]
        ),
    match = 'all')

