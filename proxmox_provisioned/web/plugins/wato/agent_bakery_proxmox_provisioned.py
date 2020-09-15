#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.gui.valuespec import (
    Alternative,
    Dictionary,
    FixedValue,
)
from cmk.gui.plugins.wato import (
    HostRulespec,
    rulespec_registry,
)
from cmk.gui.cee.plugins.wato.agent_bakery import RulespecGroupMonitoringAgentsAgentPlugins

def _valuespec_agent_config_proxmox_provisioned():
    return Alternative(
        title = _("Proxmox Provisioned Storage (Linux)"),
        help = _("This will deploy the agent plugin <tt>proxmox_provisioned</tt> for monitoring storage space."),
        style = "dropdown",
        elements = [
            Dictionary(
                title = _("Deploy plugin for Proxmox Storage"),
                elements = [
                    ("interval", Age(
                        title = _("Run asynchronously"),
                        label = _("Interval for collecting data"),
                        default_value = 300
                    )),
                ],
            ),
            FixedValue(None, title = _("Do not deploy plugin for Proxmox Storage"), totext = _("(disabled)") ),
        ]
    )

rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupMonitoringAgentsAgentPlugins,
        name="agent_config:proxmox_provisioned",
        valuespec=_valuespec_agent_config_proxmox_provisioned,
    ))

