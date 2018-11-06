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

register_notification_parameters("jira", Dictionary(
    optional_keys = ['project', 'issuetype', 'priority', 'resolution'],
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
        ("monitoring", HTTPUrl(
            title = _("Monitoring URL"),
            help = _("Configure the base URL for the Monitoring Web-GUI here. Include the site name."),
        )),
    ]
))
