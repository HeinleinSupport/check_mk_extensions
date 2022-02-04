#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

try:
    from cmk.gui.i18n import _
    from cmk.gui.plugins.wato import (
        HostRulespec,
        rulespec_registry,
    )
    from cmk.gui.cee.plugins.wato.agent_bakery.rulespecs.utils import RulespecGroupMonitoringAgentsAgentPlugins
    from cmk.gui.valuespec import DropdownChoice

    def _valuespec_agent_config_entropy_avail():
        return DropdownChoice(
            title = _("Entropy Available (Linux)"),
            help = _("This will deploy the agent plugin <tt>entropy_avail</tt> for monitoring the available entropy."),
            choices = [
                ( True, _("Deploy plugin for Entropy Check") ),
                ( None, _("Do not deploy plugin for Entropy Check") ),
            ]
        )

    rulespec_registry.register(
        HostRulespec(
            group=RulespecGroupMonitoringAgentsAgentPlugins,
            name="agent_config:entropy_avail",
            valuespec=_valuespec_agent_config_entropy_avail,
        ))

except ModuleNotFoundError:
    # RAW edition
    pass
