#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

group = "agents/" + _("Agent Plugins")

register_rule(group,
    "agent_config:postfix_procs",
    DropdownChoice(
        title = _("Postfix Processes (Linux)"),
        help = _("This will deploy the agent plugin <tt>postfix_procs</tt> for monitoring the number of Postfix processes."),
        choices = [
            ( True, _("Deploy postfix_procs plugin") ),
            ( None, _("Do not deploy postfix_procs plugin") ),
        ]
    )
)

