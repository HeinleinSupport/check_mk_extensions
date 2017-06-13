#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

group = "agents/" + _("Agent Plugins")

register_rule(group,
    "agent_config:ceph",
    DropdownChoice(
        title = _("Ceph Status (Linux)"),
        help = _("This will deploy the agent plugin <tt>ceph</tt> for monitoring the status of Ceph."),
        choices = [
            ( True, _("Deploy plugin for Ceph") ),
            ( None, _("Do not deploy plugin for Ceph") ),
        ]
    )
)

