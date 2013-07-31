#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2013 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>
#

group = "activechecks"

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


