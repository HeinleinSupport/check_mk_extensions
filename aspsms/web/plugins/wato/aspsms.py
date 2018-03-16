#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2018 Heinlein Support GmbH
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

register_notification_parameters("aspsms", Dictionary(
    optional_keys = ['originator'],
    elements = [
        ("user_key", TextAscii(
            title = _("User Key"),
            help = _("Configure the user key here. The key can be obtained from the "
                     "<a href=\"https://www.aspsms.com/apicredentials/\" target=\"_blank\">"
                     "aspsms.com</a> website."),
            size = 40,
            allow_empty = False,
        )),
        ("api_password", TextAscii(
            title = _("API Password"),
            help = _("You need to provide a valid API passowrd to be able to send notifications "
                     "using ASPSMS. Register and login to <a href=\"https://www.aspsms.com/apicredentials/\" "
                     "target=\"_blank\">ASPSMS</a> to obtain your API key."),
            size = 40,
            allow_empty = False,
        )),
        ("originator", TextAscii(
            title = _("Originator"),
            help = _("You can set the originator of the message here."),
            size = 40,
        )),
    ]
))
