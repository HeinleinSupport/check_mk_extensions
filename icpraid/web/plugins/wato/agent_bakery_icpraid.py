#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

group = "agents/" + _("Agent Plugins")

register_rule(group,
    "agent_config:icpraid",
    DropdownChoice(
        title = _("ICP RAID (Linux)"),
        help = _("This will deploy the agent plugin <tt>icpraid</tt> for monitoring the status of ICP controllers using arcconf."),
        choices = [
            ( True, _("Deploy plugin for ICP RAID") ),
            ( None, _("Do not deploy plugin for ICP RAID") ),
        ]
    )
)

