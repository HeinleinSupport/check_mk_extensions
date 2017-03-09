#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

group = "agents/" + _("Agent Plugins")

register_rule(group,
    "agent_config:aufs",
    DropdownChoice(
        title = _("aufs RW Check (Linux)"),
        help = _("This will deploy the agent plugin <tt>check_aufs</tt> which tries to create a temporary file on an aufs mount."),
        choices = [
            ( True, _("Deploy plugin for aufs.") ),
            ( None, _("Do not deploy plugin for aufs.") ),
        ]
    )
)

