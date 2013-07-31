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

register_rule(group,
    "active_checks:ssh",
    Tuple(
        title = _("Check SSH service"),
        help = _("Checks SSH. "),
        elements = [
            Dictionary(
                title = _("Optional parameters"),
                elements = [
                    ( "hostname",
                      TextAscii(
                            title = _("DNS Hostname or IP address"),
                            default_value = "$HOSTADDRESS$",
                            allow_empty = False,
                            help = _("You can specify a hostname or IP address different from IP address "
                                     "of the host as configured in your host properties."))),
                    ( 'port',
                      Integer(
                            title = _("SSH Port"),
                            help = _("Default is 22."),
                            minvalue = 1,
                            maxvalue = 65535,
                            default_value = 22)),
                    ( "ip_version",
                      Alternative(
                            title = _("IP-Version"),
                            elements = [
                                FixedValue(
                                    "ipv4",
                                    totext = "",
                                    title = _("IPv4")
                                    ),
                                FixedValue(
                                    "ipv6",
                                    totext = "",
                                    title = _("IPv6")
                                    ),
                                ],
                            )),
                    ( "timeout",
                      Integer(
                            title = _("Seconds before connection times out"),
                            unit = _("sec"),
                            default_value = 10,
                            )
                      ),
                    ( "remote-version",
                      TextAscii(
                            title = _("Remote version string to expect"),
                            help = _("Warn if string doesn't match expected server version (ex: OpenSSH_3.9p1)"),
                            size = 30)
                      ),
                    ]
                )
            ]
        ),
    match = 'all')


register_rule(group,
    "active_checks:lynx",
    Dictionary(
        title = _("Check Lynx"),
        help = _("Checks a webservice with a recorded lynx session. "),
        elements = [
                   ( "filename",
                      TextAscii(
                            title = _("Filename of Lynx-Check without .txt suffix."),
                            default_value = "$HOSTADDRESS$",
                            allow_empty = False,
                            )
                    ),
                   ( "url",
                      TextAscii(
                            title = _("URL for the webpage"),
                            allow_empty = False,
                            )
                    ),
                   ( "pattern",
                      TextAscii(
                            title = _("Pattern to search in the output."),
                            allow_empty = False,
                            )
                    ),
                   ( "description",
                      TextAscii(
                            title = _("Service Description"),
                            )
                    ),
                   
            ]
        ),
    match = 'all')


