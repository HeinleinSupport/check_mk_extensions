#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2013 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>
#

group = "activechecks"

register_rule(group,
              "active_checks:nfs",
              Tuple(
                  title = _("Check NFS export"),
                  help = _("Check NFS share size"),
                  elements = [
                      TextAscii(
                          title = _("NFS share name"),
                          allow_empty = False,
                          help = _("Name of the NFS export to check"),
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
                              ( 'warning',
                                Integer(
                                    title = _("Warning Level"),
                                    help = _("Free percentage threshold for warning."),
                                    minvalue = 0,
                                    maxvalue = 100,
                                    default_value = 20
                                    )
                                ),
                              ( 'critical',
                                Integer(
                                    title = _("Critical Level"),
                                    help = _("Free percentage threshold for critical."),
                                    minvalue = 0,
                                    maxvalue = 100,
                                    default_value = 10
                                    )
                                ),
                              ]
                          )
                      ]
                  ),
              match = 'all')

