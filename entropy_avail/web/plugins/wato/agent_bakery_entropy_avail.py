#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

group = "agents/" + _("Agent Plugins")

register_rule(group,
    "agent_config:entropy_avail",
    DropdownChoice(
        title = _("Entropy Available (Linux)"),
        help = _("This will deploy the agent plugin <tt>entropy_avail</tt> for monitoring the available entropy."),
        choices = [
            ( True, _("Deploy plugin for Entropy Check") ),
            ( None, _("Do not deploy plugin for Entropy Check") ),
        ]
    )
)

