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

def _valuespec_agent_config_postconf():
    return DropdownChoice(
        title = _("Postfix Configuration (Linux)"),
        help = _("This will deploy the agent plugin <tt>postconf</tt> for checking the Postfix configuration."),
        choices = [
            ( True, _("Deploy plugin for Postfix config") ),
            ( None, _("Do not deploy plugin for Postfix config") ),
        ]
    )

rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupMonitoringAgentsAgentPlugins,
        name="agent_config:postconf",
        valuespec=_valuespec_agent_config_postconf,
    ))
