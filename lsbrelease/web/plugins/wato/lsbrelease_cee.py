#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.gui.i18n import _
from cmk.gui.plugins.wato import (
    HostRulespec,
    rulespec_registry,
)
from cmk.gui.cee.plugins.wato.agent_bakery.rulespecs.utils import RulespecGroupMonitoringAgentsAgentPlugins
from cmk.gui.valuespec import (
    Age,
    Alternative,
    Dictionary,
    FixedValue,
)

def _valuespec_agent_config_lsbrelease():
    return Alternative(
        title = _("Distribution Version Check"),
        help = _("This will deploy the agent plugin <tt>lsbrelease</tt> for monitoring the distribution version."),
        style = "dropdown",
        elements = [
            Dictionary(
                title = _("Deploy the LSB-Release plugin"),
                elements = [
                    ( "interval", Age(title = _("Run asynchronously"), label = _("Interval for collecting data"), default_value = 300 )),
                ],
            ),
            FixedValue(None, title = _("Do not deploy the LSB-Release plugin"), totext = _("(disabled)") ),
        ]
    )

rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupMonitoringAgentsAgentPlugins,
        name="agent_config:lsbrelease",
        valuespec=_valuespec_agent_config_lsbrelease,
    ))
