#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

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

from cmk.gui.valuespec import (
    Age,
    CascadingDropdown,
    Dictionary,
    DropdownChoice,
    EmailAddress,
    FixedValue,
    HTTPUrl,
    IPv4Address,
    ListChoice,
    ListOfStrings,
    Password,
    TextAreaUnicode,
    TextAscii,
    TextUnicode,
    Transform,
    Tuple,
)

from cmk.gui.plugins.wato import (
    notification_parameter_registry,
    NotificationParameter,
)

@notification_parameter_registry.register
class NotificationParameterECityRuf(NotificationParameter):
    @property
    def ident(self):
        return "ecityruf"

    @property
    def spec(self):
        return Dictionary(
            title=_("Create notification with the following parameters"),
            elements=[
                ("from", EmailAddress(
                    title=_("From: Address"),
                    size=40,
                    allow_empty=False,
                )),
                ("host_subject",
                 TextUnicode(
                     title=_("Subject for host notifications"),
                     help=_("Here you are allowed to use all macros that are defined in the "
                            "notification context."),
                     default_value="Check_MK: $HOSTNAME$ - $EVENT_TXT$",
                     size=64,
                 )),
                ("service_subject",
                 TextUnicode(
                     title=_("Subject for service notifications"),
                     help=_("Here you are allowed to use all macros that are defined in the "
                            "notification context."),
                     default_value="Check_MK: $HOSTNAME$/$SERVICEDESC$ $EVENT_TXT$",
                     size=64,
                 )),
                ("common_body",
                 TextAreaUnicode(
                     title=_("Body head for both host and service notifications"),
                     rows=7,
                     cols=58,
                     monospaced=True,
                     default_value="""Host:     $HOSTNAME$
Alias:    $HOSTALIAS$
Address:  $HOSTADDRESS$
""",
                 )),
                ("host_body",
                 TextAreaUnicode(
                     title=_("Body tail for host notifications"),
                     rows=9,
                     cols=58,
                     monospaced=True,
                     default_value="""Event:    $EVENT_TXT$
Output:   $HOSTOUTPUT$
Perfdata: $HOSTPERFDATA$
$LONGHOSTOUTPUT$
""",
                 )),
                ("service_body",
                 TextAreaUnicode(
                     title=_("Body tail for service notifications"),
                     rows=11,
                     cols=58,
                     monospaced=True,
                     default_value="""Service:  $SERVICEDESC$
Event:    $EVENT_TXT$
Output:   $SERVICEOUTPUT$
Perfdata: $SERVICEPERFDATA$
$LONGSERVICEOUTPUT$
""",
                 )),
            ],
        )

