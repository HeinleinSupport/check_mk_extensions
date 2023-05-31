#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2019 Heinlein Support GmbH
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

from cmk.gui.plugins.wato.active_checks.common import ip_address_family_element
from cmk.gui.plugins.wato.utils import IndividualOrStoredPassword
from cmk.gui.valuespec import (
    Alternative,
    Checkbox,
    Dictionary,
    DropdownChoice,
    Integer,
    ListOf,
    RegExp,
    TextInput,
    TextUnicode,
    Tuple,
)

register_rule("activechecks",
              "active_checks:restapi",
              Dictionary(
                  title = _("Check REST API"),
                  help = _("Checks REST API with <tt>check_http</tt>."),
                  elements = [
                      ('name', TextUnicode(
                          title = _("Name"),
                          help = _("Will be used in the service description. If the name starts with "
                                   "a caret (<tt>^</tt>), the service description will not be prefixed with "
                                  "<tt>REST API</tt>." ),
                          allow_empty = False)),
                      ('method', DropdownChoice(
                          title = _("Method"),
                          choices = [
                              ('GET', 'GET'),
                              ('HEAD', 'HEAD'),
                              ],
                          default_value = "GET",
                          )),
                      ( "virthost",
                                    Tuple(
                                        title = _("Virtual host"),
                                        elements = [
                                            TextInput(
                                                title = _("Name of the virtual host"),
                                                help = _("Set this in order to specify the name of the "
                                                         "virtual host for the query (using HTTP/1.1). If you "
                                                         "leave this empty, then the IP address of the host "
                                                         "will be used instead."),
                                                allow_empty = False
                                            ),
                                            Checkbox(
                                                label = _("Omit specifying an IP address"),
                                                help = _("Usually Check_MK will nail this check to the "
                                                         "IP address of the host it is attached to. With this "
                                                         "option you can have the check use the name of the "
                                                         "virtual host instead and do a dynamic DNS lookup."),
                                                true_label = _("omit IP address"),
                                                false_label = _("specify IP address"),
                                            ),
                                        ]
                                    )
                                ),
                      ( "port", Integer(
                          title = _("TCP Port"),
                          minvalue = 1,
                          maxvalue = 65535,
                          default_value = 80
                       )),
                      ('ssl', Checkbox(
                          title = _('SSL'),
                          label = _('Use SSL and SNI'),
                          default_value = True,
                          )),
                      ip_address_family_element(),
                      ('uri', TextInput(
                          title = _("URI to fetch (default is <tt>/</tt>)"),
                          allow_empty = False,
                          default_value = "/"
                       )),
                      ('auth', Alternative(
                          title = _("Authentication"),
                          elements = [
                              IndividualOrStoredPassword(title = _("API Token")),
                              Tuple(title = _("Credentials"),
                                    elements = [
                                        TextInput(title=_("Username")),
                                        IndividualOrStoredPassword(title=_("Password")),
                                        ],
                                    ),
                              ])),
                      ('header', ListOf(
                          Tuple(
                              title = _("Header"),
                              elements = [
                                  TextInput(title = _("Name")),
                                  TextInput(title = _("Value"))
                                  ],
                              orientation = 'horizontal',
                              ),
                          title = _('Additional Headers'),
                        )),
                      ("expect_response_header", TextInput(
                          title = _("String to expect in response headers"),
                          )),
                      ( "expect_regex",
                          Tuple(
                              title = _("Regular expression to expect in content"),
                              orientation = "vertical",
                              show_titles = False,
                              elements = [
                                  RegExp(
                                      label = _("Regular expression: "),
                                      mode = RegExp.infix,
                                  ),
                                  Checkbox(label = _("Case insensitive")),
                                  Checkbox(label = _("return CRITICAL if found, OK if not")),
                                  Checkbox(label = _("Multiline string matching")),
                              ]
                          )),
                      ],
                      required_keys = ['name'],
                  ),
              match = 'all')
