#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

group = "agents/" + _("Agent Plugins")

register_rule(group,
    "agent_config:ox_runtimestats",
    DropdownChoice(
        title = _("Open-Xchange runtime statistics (Linux)"),
        help = _("This will deploy the agent plugin <tt>ox_runtimestats</tt> for monitoring Open-Xchange."),
        choices = [
            ( True, _("Deploy plugin for Open-Xchange") ),
            ( None, _("Do not deploy plugin for Open-Xchange") ),
        ]
    )
)

