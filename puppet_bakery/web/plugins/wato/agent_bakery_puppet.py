#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

group = "agents/" + _("Agent Plugins")

register_rule(group,
    "agent_config:puppet",
    DropdownChoice(
        title = _("Puppet Agent Checks (Linux)"),
        help = _("This will deploy the agent plugin <tt>mk_puppet</tt>."),
        choices = [
            ( True, _("Deploy plugin for Puppet Agent.") ),
            ( None, _("Do not deploy plugin for Puppet Agent.") ),
        ]
    )
)

