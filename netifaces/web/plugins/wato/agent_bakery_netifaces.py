#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

group = "agents/" + _("Agent Plugins")

register_rule(group,
    "agent_config:netifaces",
    DropdownChoice(
        title = _("Network Interface Addresses (Linux)"),
        help = _("This will deploy the agent plugin <tt>netifaces</tt> that returns the list of addresses configured."),
        choices = [
            ( True, _("Deploy plugin for Network Interface Addresses") ),
            ( None, _("Do not deploy plugin for Network Interface Addresses") ),
        ]
    )
)

