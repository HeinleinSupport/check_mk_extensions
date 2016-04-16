#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

group = "agents/" + _("Agent Plugins")

register_rule(group,
    "agent_config:filehandles",
    DropdownChoice(
        title = _("Filehandles (Linux)"),
        help = _("This will deploy the agent plugin <tt>filehandles</tt> for monitoring the number of allocated file handles."),
        choices = [
            ( True, _("Deploy filehandles plugin") ),
            ( None, _("Do not deploy filehandles plugin") ),
        ]
    )
)

