#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2013 Heinlein Support GmbH
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

group = "activechecks"

register_rule(group,
              "active_checks:imap",
              Dictionary(
                  title = _("Check IMAP"),
                  help = _("Checks IMAP values"),
                  elements = [
                      ( "hostname",
                        TextAscii(title = _("DNS Hostname or IP address"),
                                  default_value = "$HOSTADDRESS$",
                                  ),
                        ),
                      ( "port",
                        Integer(title = _("Port number"),
                                minvalue = 1,
                                maxvalue = 65535,
                                default_value = 143,
                                ),
                        ),
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
                      ( "send",
                        TextAscii(
                            title = _("String to send to the server"),
                            ),
                        ),
                      ( "expect",
                        TextAscii(
                            title = _("String to expect in server response"),
                            ),
                        ),
                      ( "quit",
                        TextAscii(
                            title = _("String to send server to initiate a clean close of the connection"),
                            ),
                        ),
                      ( "refuse",
                        DropdownChoice(
                            title = _("Accept TCP refusals with states ok, warn, crit"),
                            choices = [ ('crit', _("CRITICAL")),
                                        ('warn', _("WARNING")),
                                        ('ok',   _("OK")),
                                        ],
                            default_value = 'crit',
                            )
                        ),
                      ( "mismatch",
                        DropdownChoice(
                            title = _("Accept expected string mismatches with states ok, warn, crit"),
                            choices = [ ('crit', _("CRITICAL")),
                                        ('warn', _("WARNING")),
                                        ('ok',   _("OK")),
                                        ],
                            default_value = 'warn',
                            )
                        ),
                      ( "jail",
                        FixedValue(
                            "jail",
                            title = _("Hide output from TCP socket"),
                            totext = "",
                            ),
                        ),
                      ( "maxbytes",
                        Integer(
                            title = _("Close connection once more than this number of bytes are received"),
                            ),
                        ),
                      ( "delay",
                        Integer(
                            title = _("Seconds to wait between sending string and polling for response"),
                            ),
                        ),
                      ( "ssl",
                        FixedValue (
                            "ssl",
                            title = _("Use SSL for the connection"),
                            totext = "",
                            ),
                        ),
                      ( "certificate_age",
                        Tuple (
                            title = _("Minimum number of days a certificate has to be valid."),
                            elements = [
                                Integer(
                                    title = _("Warning"),
                                    default_value = 60,
                                    unit = _("days"),
                                    ),
                                Integer(
                                    title = _("Critical"),
                                    default_value = 90,
                                    unit = _("days"),
                                    ),
                                ],
                            ),
                        ),
                      ( "warning",
                        Integer(
                            title = _("Response time to result in warning status"),
                            unit = _("sec"),
                            default_value = 10,
                            )
                        ),
                      ( "timeout",
                        Integer(
                            title = _("Response time to result in critical status"),
                            unit = _("sec"),
                            default_value = 15,
                            )
                        ),
                      ( "timeout",
                        Integer(
                            title = _("Seconds before connection times out"),
                            unit = _("sec"),
                            default_value = 10,
                            )
                        ),
                      ]
                  ),
              match = 'all'
              )

