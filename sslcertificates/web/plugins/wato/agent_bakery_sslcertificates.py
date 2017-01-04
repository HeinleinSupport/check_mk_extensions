#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

register_rule(
    "agents/" + _("Agent Plugins"),
    "agent_config:sslcertificates",
    Alternative(
        title = _("SSL Certificates"),
        help = _("This will deploy the agent plugin <tt>sslcertificates</tt> "
                 "for checking SSL certificate files. <b>Note:</b> If you want "
                 "to configure several directories to look into for SSL certificate "
                 "files, then simply create several rules. In this ruleset "
                 "<b>all</b> matching rules "
                 "are being executed, not only the first one. "),
        style = "dropdown",
        elements = [
            Dictionary(
                title = _("Deploy the SSL certificates plugin"),
                elements = [
                   ( "directories",
                     ListOfStrings(
                        title = _("Directories to look into for SSL certificate files"),
                        valuespec = TextAscii(
                            size = 80,
                            regex = "^/[^ \t]+$",
                            regex_error = _("Directory paths must begin with <tt>/</tt> and must not contain spaces."),
                       ),
                       allow_empty = False,

                     )
                   ),
                ],
                optional_keys = False,
            ),
            FixedValue(None, title = _("Do not deploy the SSL certificates plugin"), totext = _("(disabled)") ),
        ]
    ),
    match = "all",
)

