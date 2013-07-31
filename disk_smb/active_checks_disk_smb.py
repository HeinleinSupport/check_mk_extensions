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
              "active_checks:disk_smb",
              Tuple(
                  title = _("Check SMB share"),
                  help = _("Checks SMB share size"),
                  elements = [
                      TextAscii(
                          title = _("SMB share name"),
                          allow_empty = False,
                          help = _("Name of the SMB share to check"),
                          ),
                      Dictionary(
                          title = _("Optional arguments"),
                          elements = [
                              ( "hostname",
                                TextAscii(
                                    title = _("DNS Hostname or IP address"),
                                    default_value = "$HOSTADDRESS$",
                                    allow_empty = False,
                                    help = _("You can specify a hostname or IP address different from IP address "
                                             "of the host as configured in your host properties.")
                                    )
                                ),
                              ( "workgroup",
                                TextAscii(
                                    title = _("Windows Workgroup"),
                                    default_value = "$USER7$",
                                    )
                                ),
                              ( "user",
                                TextAscii(
                                    title = _("User name"),
                                    default_value = "guest",
                                    )
                                ),
                              ( "password",
                                TextAscii(
                                    title = _("Password"),
                                    default_value = "$USER6$",
                                    )
                                ),
                              ( 'warning',
                                Integer(
                                    title = _("Warning Level"),
                                    help = _("Used percentage threshold for warning."),
                                    minvalue = 0,
                                    maxvalue = 100,
                                    default_value = 85
                                    )
                                ),
                              ( 'critical',
                                Integer(
                                    title = _("Critical Level"),
                                    help = _("Used percentage threshold for critical."),
                                    minvalue = 0,
                                    maxvalue = 100,
                                    default_value = 95
                                    )
                                ),
                              ]
                          )
                      ]
                  ),
              match = 'all'
              )

