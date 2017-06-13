#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

group = "agents/" + _("Agent Plugins")

register_rule(group,
    "agent_config:lvm",
    DropdownChoice(
        title = _("LVM Status (Linux)"),
        help = _("This will deploy the agent plugin <tt>lvm</tt> for monitoring the status of LVM PVs and VGs."),
        choices = [
            ( True, _("Deploy plugin for LVM") ),
            ( None, _("Do not deploy plugin for LVM") ),
        ]
    )
)

