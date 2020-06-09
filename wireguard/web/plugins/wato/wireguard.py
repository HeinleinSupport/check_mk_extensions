#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

register_rule("agents/" + _("Agent Plugins"),
    "agent_config:wireguard",
    DropdownChoice(
        title = _("WireGuard VPN (Linux)"),
        help = _("This will deploy the agent plugin <tt>wireguard</tt> for monitoring the status of WireGuard VPNs."),
        choices = [
            ( True, _("Deploy plugin for WireGuard VPNs") ),
            ( None, _("Do not deploy plugin for WireGuard VPNs") ),
        ]
    )
)
