#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.gui.valuespec import DropdownChoice
from cmk.gui.plugins.wato import HostRulespec
from cmk.gui.cee.plugins.wato.agent_bakery import RulespecGroupMonitoringAgentsAgentPlugins

def _valuespec_agent_config_proxmox_provisioned():
    return DropdownChoice(
        title = _("Proxmox Provisioned Storage (Linux)"),
        help = _("This will deploy the agent plugin <tt>proxmox_provisioned</tt> for monitoring storage space."),
        choices = [
            ( True, _("Deploy plugin for Proxmox Storage") ),
            ( None, _("Do not deploy plugin for Proxmox Storage") ),
        ]
    )

rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupMonitoringAgentsAgentPlugins,
        name="agent_config:proxmox_provisioned",
        valuespec=_valuespec_agent_config_proxmox_provisioned,
    ))

