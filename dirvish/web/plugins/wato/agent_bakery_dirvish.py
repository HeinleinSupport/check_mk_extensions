#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

group = "agents/" + _("Agent Plugins")

register_rule(group,
    "agent_config:dirvish",
    Alternative(
        title = _("Dirvish Backup Status (Linux)"),
        help = _("This will deploy the agent plugin <tt>dirvish</tt> "
                 "for checking Dirvish Backup status."),
        style = "dropdown",
        elements = [
            Dictionary(
                title = _("Deploy the Dirvish plugin"),
                elements = [
                   ( "bank",
                     TextAscii(
                       title = _("Dirvish Bank directory"),
                       size = 80,
                       regex = "^/[^ \t*]+$",
                       regex_error = _("Directory path must begin with <tt>/</tt> and must not contain spaces."),
                       allow_empty = False,
                     ),
                   ),
                ],
                optional_keys = False,
            ),
            FixedValue(None, title = _("Do not deploy the Dirvish plugin"), totext = _("(disabled)") ),
        ]
    ),
)

