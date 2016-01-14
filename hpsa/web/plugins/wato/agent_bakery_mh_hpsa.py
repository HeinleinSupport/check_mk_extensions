#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

group = "agents/" + _("Agent Plugins")

register_rule(group,
    "agent_config:mh_hpsa",
    DropdownChoice(
        title = _("HP RAID Controller Status (Linux)"),
        help = _("This will deploy the agent plugin <tt>mh_hpsa</tt> for monitoring the status of HP Raid controllers via hpacucli."),
        choices = [
            ( True, _("Deploy plugin for HP RAID controllers") ),
            ( None, _("Do not deploy plugin for HP RAID controllers") ),
        ]
    )
)

