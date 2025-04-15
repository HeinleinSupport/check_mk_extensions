#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2018 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2. This file is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# tails. You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

from cmk.gui.valuespec import (
    Dictionary,
    HTTPUrl,
    Integer,
    Password,
    TextAscii,
    TextInput,
)
from cmk.gui.wato import register_notification_parameters
from cmk.gui.i18n import _

register_notification_parameters("jira_heinlein", Dictionary(
    optional_keys = ['project', 'issuetype', 'priority', 'resolution', 'add_customfield', 'add_customvalue'],
    elements = [
        ("url", HTTPUrl(
            title = _("JIRA URL"),
            help = _("Configure the JIRA URL here."),
        )),
        ("username", TextAscii(
            title = _("User Name"),
            help = _("Configure the user name here."),
            size = 40,
            allow_empty = False,
        )),
        ("password", Password(
            title = _("Password"),
            help = _("You need to provide a valid passowrd to be able to send notifications."),
            size = 40,
            allow_empty = False,
        )),
        ("project", Integer(
            title = _("Project ID"),
            help = _("The numerical JIRA project ID. If not set, it will be retrieved from a custom user attribute named <tt>jiraproject</tt>. If that is not set, the notification will fail."),
        )),
        ("issuetype", Integer(
            title = _("Issue type ID"),
            help = _("The numerical JIRA issue type ID. If not set, it will be retrieved from a custom user attribute named <tt>jiraissuetype</tt>. If that is not set, the notification will fail."),
        )),
        ("priority", Integer(
            title = _("Priority ID"),
            help = _("The numerical JIRA priority ID. If not set, it will be retrieved from a custom user attribute named <tt>jirapriority</tt>. If that is not set, the standard priority will be used."),
        )),
        ("resolution", Integer(
            title = _("Resultion Transistion ID"),
            help = _("The numerical JIRA resolution transition ID. If not set, it will be retrieved from a custom user attribute named <tt>jiraresolution</tt>."),
        )),
        ("add_customfield", TextInput(
            title = _("Additional custom field name"),
            help=_("The numerical ID of an additional Jira custom field that should be set in the issue. If not set, it can be retrieved from a custom user attribute named <tt>jiraaddcf</tt>."),
        )),
        ("add_customvalue", TextInput(
            title=_("Additional custom field value"),
            help=_("The value of the additional Jira custom field. If not set, it can be retrieved from a custom user attribute named <tt>jiraaddcfval</tt>."),
        )),
        ("monitoring", HTTPUrl(
            title = _("Monitoring URL"),
            help = _("Configure the base URL for the Monitoring Web-GUI here. Include the site name."),
        )),
    ]
))
