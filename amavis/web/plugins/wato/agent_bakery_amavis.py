#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

group = "agents/" + _("Agent Plugins")

register_rule(group,
    "agent_config:amavis",
    DropdownChoice(
        title = _("Amavis (Linux)"),
        help = _("This will deploy the agent plugin <tt>amavis</tt> to check various amavisd-new stats."),
        choices = [
            ( True, _("Deploy plugin for amavisd-new") ),
            ( None, _("Do not deploy plugin for amavisd-new") ),
        ]
    )
)

