#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2013 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>
#

group = "activechecks"

register_rule(group,
              "active_checks:ups",
              Dictionary(
                  title = _("Check UPS"),
                  help = _("Checks UPS values"),
                  elements = [
                      ( "hostname",
                        TextAscii(title = _("DNS Hostname or IP address"),
                                  default_value = "$HOSTADDRESS$",
                                  ),
                        ),
                      ( "upsname",
                        TextAscii(title = _("UPS Name"),
                                  allow_empty = False,
                                  ),
                        ),
                      ( "port",
                        Integer(title = _("Port number"),
                                minvalue = 1,
                                maxvalue = 65535,
                                default_value = 3493,
                                ),
                        ),
                      ]
                  ),
              match = 'all'
              )

