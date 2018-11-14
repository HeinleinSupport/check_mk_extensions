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

register_rule(
    "agents/" + _("Agent Plugins"),
    "agent_config:sap_hana",
    Alternative(
        title = _("SAP HANA"),
        help = _("This will deploy the agent plugin <tt>sap_hana</tt> "
                 "for checking various SAP HANA parameters"),
        style = "dropdown",
        elements = [
            Dictionary(
                title = _("Deploy the SAP HANA plugin"),
                elements = [
                   ( "auth",
                     CascadingDropdown(
                         title = _("Authentication method"),
                         choices = [
                             ( "explicit",
                               _("Login with the following credentials"),
                               Tuple(
                                   elements = [
                                       TextAscii(title = _("User"), size=30, forbidden_chars=":$'\"", allow_empty=False),
                                       IndividualOrStoredPassword(title = _("Password"), size=16, forbidden_chars=":$'\"", allow_empty=False),
                                   ]
                               )),
                            ( "store",
                              _("Use a Userstore"),
                              Tuple(
                                   elements = [
                                       TextAscii(title = _("Userstore Key"), size=30, forbidden_chars=":$'\"", allow_empty=False),
                                   ]
                              )
                            )
                        ]
                    )),
                    ( "runas",
                      DropdownChoice(
                          title = _("Run As"),
                          help = _("Run hdbsql as agent user (usually root) or SAP HANA instance user. This is important when using the userstore authentication method."),
                          choices = [
                              ( "instance", _("SAP HANA Instance User")),
                              ( "agent", _("Check_MK Agent User (usually root)")),
                          ],
                          default_value = "instance",
                    )),
                ],
                optional_keys = 'runas',
            ),
            FixedValue(None, title = _("Do not deploy the SAP HANA plugin"), totext = _("(disabled)") ),
        ]
    ),
    match = "first",
)

