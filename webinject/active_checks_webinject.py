#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2013 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>
#

group = "activechecks"

register_rule(group,
    "active_checks:webinject",
    Tuple(
        title = _("Check Web service with Webinject"),
        help = _("Check the result of several Webinject tests. "
                 "This check uses <tt>check_webinject</tt> from the local Nagios plugins."),
        elements = [
           TextAscii(title = _("Hostname"), allow_empty = False,
                     help = _('The name of the (virtual) host with the configuration in ~/etc/webinject/hostname.xml')),
        ]
    ),
    match = 'all')

