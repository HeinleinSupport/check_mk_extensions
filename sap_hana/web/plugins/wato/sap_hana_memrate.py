#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) Robert Sander <r.sander@heinlein-support.de>

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

register_check_parameters(
    subgroup_applications,
    "sap_hana_memrate",
    _("SAP HANA Memory Usage"),
    Transform(
        Dictionary(
            help = _("Memory levels for SAP HANA instances"),
            elements = [
                ("levels", CascadingDropdown(
                    title = _("Levels for memory usage"),
                    choices = [
                        ( "perc_used",
                          _("Percentual levels for used memory"),
                          Tuple(
                              elements = [
                                   Percentage(title = _("Warning at a memory usage of"), default_value = 70.0),
                                   Percentage(title = _("Critical at a memory usage of"), default_value = 80.0)
                              ]
                        )),
                        ( "abs_free",
                          _("Absolute levels for free memory"),
                          Tuple(
                              elements = [
                                 Filesize(title = _("Warning below")),
                                 Filesize(title = _("Critical below"))
                              ]
                        )),
                        ( "ignore", _("Do not impose levels")),
                    ])
                ),
            ],
            optional_keys = [],
        ),
    ),
    TextAscii(
        title = _("SAP HANA instance"),
        allow_empty = False,
    ),
    "dict",
)
