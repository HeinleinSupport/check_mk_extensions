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
    "active_checks:by_ssh",
    Tuple(
        title = _("Check via SSH service"),
        help = _("Checks via SSH. "),
        elements = [
            TextAscii(
                title = _("Command"),
                help = _("Command to execute on remote host."),
                allow_empty = False,
            ),
            Dictionary(
                title = _("Optional parameters"),
                elements = [
                    ( "description",
                      TextAscii(
                          title = _("Service Description"),
                          help = _("Must be unique for every host. Defaults to command that is executed."),
                          size = 30)
                      ),
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
                    ( "logname",
                      TextAscii(
                          title = _("Username"),
                          help = _("SSH user name on remote host"),
                          size = 30)
                      ),
                    ( "identity",
                      TextAscii(
                          title = _("Keyfile"),
                          help = _("Identity of an authorized key"),
                          size = 30)
                      ),
                    ]
                )
            ]
        ),
    match = 'all')

