#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

register_rule("agents/" + _("Agent Plugins"),
    "agent_config:wireguard",
    DropdownChoice(
        title = _("Wireguard VPN (Linux)"),
        help = _("This will deploy the agent plugin <tt>wireguard</tt> for monitoring the status of Wireguard VPNs."),
        choices = [
            ( True, _("Deploy plugin for Wireguard VPNs") ),
            ( None, _("Do not deploy plugin for HP RAID controllers") ),
        ]
    )
)
