#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2013 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>
#

group = "activechecks"

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

