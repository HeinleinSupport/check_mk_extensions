#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

group = "agents/" + _("Agent Plugins")

register_rule(group,
    "agent_config:postconf",
    DropdownChoice(
        title = _("Postfix Configuration (Linux)"),
        help = _("This will deploy the agent plugin <tt>postconf</tt> for checking the Postfix configuration."),
        choices = [
            ( True, _("Deploy plugin for Postfix config") ),
            ( None, _("Do not deploy plugin for Postfix config") ),
        ]
    )
)

