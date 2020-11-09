#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.gui.cee.plugins.wato.agent_bakery import RulespecGroupMonitoringAgentsAgentPlugins

def _valuespec_agent_config_updater_hostname():
    return DropdownChoice(
        title=_("Agent Updater Hostname (Linux)"),
        help=_("Hosts configured via this rule get the <tt>updater_hostname</tt> plugin "
               "deployed. This will create a service check that compares the host's name "
               "with the value in /etc/cmk-update-agent.state."),
        choices=[
            (True, _("Deploy Updater Hostname plugin")),
            (None, _("Do not deploy Updater Hostname plugin")),
        ],
    )


rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupMonitoringAgentsAgentPlugins,
        name="agent_config:updater_hostname",
        valuespec=_valuespec_agent_config_updater_hostname,
    ))
