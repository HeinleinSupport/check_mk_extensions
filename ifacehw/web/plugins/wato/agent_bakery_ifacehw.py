#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

group = "agents/" + _("Agent Plugins")

register_rule(group,
    "agent_config:ifacehw",
    DropdownChoice(
        title = _("Network Interface Hardware (Linux)"),
        help = _("This will deploy the agent plugin <tt>ifacehw</tt>. This check if a e1000 or pcnet32 adapters are used on virtual hardware."),
        choices = [
            ( True, _("Deploy ifacehw plugin") ),
            ( None, _("Do not deploy ifacehw plugin") ),
        ]
    )
)

