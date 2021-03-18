#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.gui.i18n import _
from cmk.gui.plugins.wato import (
    HostRulespec,
    rulespec_registry,
)
from cmk.gui.cee.plugins.wato.agent_bakery.rulespecs.utils import RulespecGroupMonitoringAgentsAgentPlugins
from cmk.gui.valuespec import (
    DropdownChoice,
)

def _valuespec_agent_config_ox_runtimestats():
    return DropdownChoice(
        title = _("Open-Xchange runtime statistics (Linux)"),
        help = _("This will deploy the agent plugin <tt>ox_runtimestats</tt> for monitoring Open-Xchange."),
        choices = [
            ( True, _("Deploy plugin for Open-Xchange") ),
            ( None, _("Do not deploy plugin for Open-Xchange") ),
        ]
    )

rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupMonitoringAgentsAgentPlugins,
        name="agent_config:ox_runtimestats",
        valuespec=_valuespec_agent_config_ox_runtimestats,
    ))
